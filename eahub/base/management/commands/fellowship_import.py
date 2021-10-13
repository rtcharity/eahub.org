import pandas

from eahub.profiles.models import Profile, VisibilityEnum, Membership, ProfileTag, ProfileTagType, ProfileTagTypeEnum
from eahub.localgroups.models import LocalGroup
from eahub.base.models import User
from django.core.management import base

class Command(base.BaseCommand):
  def handle(self, *args, **options):
      headers = pandas.read_csv("data/test_book.csv", index_col=0, nrows=0).columns.tolist()
      users_from_csv = pandas.read_csv(f"data/test_book.csv")
      count_saved = 0
      count_skipped = 0
      for i, row in users_from_csv.iterrows():
          email = row["email"]
          if User.objects.filter(email=email):
            count_skipped += 1
            print(f"User with email {email} already exists")
          else:
            user = User()
            user.email = email
            user.save()
            profile = Profile(user=user)
            profile.save()
            for header in headers:
              value = row[header]
              if header == "local_groups":
                group = LocalGroup.objects.filter(name=value)
                if group:
                  m = Membership(profile=profile, local_group=group[0])
                  m.save()
              elif "tag" in header:
                tag_name = header.replace("tags_", "")
                profile_tag_type_enum = ProfileTagTypeEnum(tag_name)
                profile_tag_types = ProfileTagType.objects.filter(type=profile_tag_type_enum)
                profile_tag_type = profile_tag_types[0]
                if not profile_tag_types:
                  print(f"Tag {tag_name} does not exist")
                  continue
                if not isinstance(value, str):
                  continue
                for single_value in value.split(","):
                  profile_tags = ProfileTag.objects.filter(name=single_value)
                  if profile_tags:
                    for profile_tag in profile_tags:
                      tag_prop = getattr(profile, header)
                      tags_on_profile = list(tag_prop.all())
                      tags_on_profile.append(profile_tag)
                      tag_prop.set(tags_on_profile)
                      if not profile_tag.types.filter(type=profile_tag_type_enum).exists():
                        types_prop = list(profile_tag.types.all())
                        types_prop.append(profile_tag_type)
                        profile_tag.types.set(types_prop)
                  else:
                    profile_tag = ProfileTag(name=single_value,author=profile)
                    profile_tag.save()
                    profile_tag.types.set([profile_tag_type])
                    profile_tag.save()
              else:
                profile.__dict__[header] = row[header]
            profile.visibility = VisibilityEnum.PRIVATE
            profile.is_approved = True
            profile.save()
            count_saved += 1
            print(f"Save user with email {email}")

      print(f"Saved {count_saved} users, skipped {count_skipped} users")


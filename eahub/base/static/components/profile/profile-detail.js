document.addEventListener('DOMContentLoaded', () => {
  for (const popoverElems of document.querySelectorAll('[data-bs-toggle="popover"]')) {
    new bootstrap.Popover(popoverElems);
  }
});

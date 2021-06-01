import {AxiosResponse} from 'axios';
import axios from 'axios';
import Cookies from 'js-cookie';


export default class HttpService {
    csrfToken: string
    
    constructor() {
        this.csrfToken = Cookies.get('csrftoken');
    }
    
    async get(url: string): Promise<AxiosResponse> {
        return await axios.get(url);
    }

    async patch(url: string, data: any): Promise<AxiosResponse> {
        return await axios.patch(
            url,
            data,
            {
                headers: {'X-CSRFToken': Cookies.get('csrftoken')}
            }
        );
    }

    async post(url: string, data: any): Promise<AxiosResponse> {
        return await axios.post(
            url,
            data,
            {
                headers: {'X-CSRFToken': Cookies.get('csrftoken')}
            }
        );
    }
}

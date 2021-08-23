class Api {
    constructor(apiUrl) {
        this.apiUrl =  apiUrl;
    }

    getLicense  (text)  {
        return fetch(`${this.apiUrl}/licenses?search=${text}`, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
            }
        })
            .then( e => {
                if(e.ok) {
                    return e.json()
                }
                return Promise.reject(e.statusText)
            })
    }
}
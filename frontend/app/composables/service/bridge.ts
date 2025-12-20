export class bridge {
    constructor() {
        console.log('Bridge instance created')
    }
    url: string = "http://127.0.0.1:5080";
    jwt: string = "";

    setjwt(new_jwt: string) {
        this.jwt = new_jwt;
    }

    getjwt() {
        return this.jwt;
    }

    async login(credential: string | undefined) {
        try {
            const response = await fetch(this.url + `/user/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + credential
                },
            });
            if (response.ok) {
                if (credential) {
                    this.setjwt(credential)
                    return await response.json();
                }
            }
            const errBody = await response.json();
            throw { status: response.status, body: errBody };
        } catch (err) {
            console.error('Network / fetch error login', err);
            throw err;
        }
    }
}
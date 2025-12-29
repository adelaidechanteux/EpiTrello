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
                    return { status: response.status, success: true };

                }
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / fetch error login', err);
            throw err;
        }
    }

    async getBoards(userID: string) {
        try {
            const response = await fetch(this.url + `/get/board/` + userID + `/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer' + this.jwt
                },
            });
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / fetch boards error', err);
            throw err;
        }
    }

    async createBoard(boardName: string) {
        try {
            const response = await fetch(this.url + `/create/board/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
                body: JSON.stringify(boardName)
            });
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / create board error', err);
            throw err;
        }
    }

    async deleteBoard(boardID: string) {
        try {
            const response = await fetch(this.url + `/delete/board/` + boardID, {
                method: 'POST',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
            });
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / delete board error', err);
            throw err;
        }
    }

    async createTask(boardID: string, data: any) {
        try {
            const response = await fetch(this.url + `/create/task/` + boardID + `/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / create task error', err);
            throw err;
        }
    }

    async deleteTask(boardID: string, taskID: string) {
        try {
            const response = await fetch(this.url + `/delete/task/` + boardID + `/` + taskID + `/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
            })
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / delete task error', err);
            throw err;
        }
    }

    async deleteArchive(boardID: string, taskID: string) {
        try {
            const response = await fetch(this.url + `/deleteforce/task/` + boardID + `/` + taskID + `/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
            })
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / delete task error', err);
            throw err;
        }
    }

    async updateTask(taskID: string, data: any) {
        try {
            const response = await fetch(this.url + `/update/task/` + taskID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'appliaction/json',
                    'Authorization': 'Bearer' + this.jwt
                },
                body: JSON.stringify(data)
            })
            if (response.ok) {
                return { status: response.status, success: true };
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / delete task error', err);
            throw err;
        }
    }
}
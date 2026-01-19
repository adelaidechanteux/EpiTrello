export class bridge {
    constructor() {
        console.log('Bridge instance created')
    }
    url: string = "http://127.0.0.1:5081";
    jwt: string = "";

    setjwt(new_jwt: string) {
        this.jwt = new_jwt;
    }

    getjwt() {
        return this.jwt;
    }

    async login(credential: string | undefined) {
        try {
            const response = await fetch(this.url + `/v2/auth/user/login/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + credential
                },
            });
            console.log(credential)
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

    async getBoardData(boardID: string) {
        try {
            const response = await fetch(this.url + `/v2/board/get/board/` + boardID + `/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
            });
            if (response.ok) {
                return await response.json();
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / fetch boards error', err);
            throw err;
        }
    }

    async getBoards() {
        try {
            const response = await fetch(this.url + `/v2/board/boards/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
            });
            if (response.ok) {
                return await response.json();
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / fetch boards error', err);
            throw err;
        }
    }

    async InviteBoard(boardID: string, email: string, admin: boolean) {
        try {
            const response = await fetch(this.url + `/v2/board/invit/board/` + boardID + `/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
                body: JSON.stringify({ email: email, admin: admin }),
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

    async createBoard(boardName: string) {
        try {
            const response = await fetch(this.url + `/v2/board/create/board/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
                body: JSON.stringify({ title: boardName }),
            });
            if (response.ok) {
                return await response.json();
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / create board error', err);
            throw err;
        }
    }

    async deleteBoard(boardID: string) {
        try {
            const response = await fetch(this.url + `/v2/board/delete/board/` + boardID, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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
            const response = await fetch(this.url + `/v2/board/create/task/` + boardID + `/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
                body: JSON.stringify(data)
            });
            if (response.ok) {
                return await response.json();
            }
            throw { status: response.status, success: false };
        } catch (err) {
            console.error('Network / create task error', err);
            throw err;
        }
    }

    async deleteTask(boardID: string, taskID: string) {
        try {
            const response = await fetch(this.url + `/v2/board/delete/task/` + boardID + `/` + taskID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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
            const response = await fetch(this.url + `/v2/board/deleteforce/task/` + boardID + `/` + taskID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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

    async updateTask(boardID: string, taskID: string, data: any) {
        try {
            const response = await fetch(this.url + `/v2/board/update/task/` + boardID + `/` + taskID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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

    async updateBoard(boardID: string, data: any) {
        try {
            const response = await fetch(this.url + `/v2/board/update/board/` + boardID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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

    async deleteMember(boardID: string, email: string) {
        try {
            const response = await fetch(this.url + `/v2/board/delete/member/` + boardID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
                },
                body: JSON.stringify({ email: email })
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

    async updateCategories(boardID: string, data: any) {
        try {
            const response = await fetch(this.url + `/v2/board/update/categories/` + boardID + `/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + this.jwt
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
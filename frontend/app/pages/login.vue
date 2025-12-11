<template>
    <UContainer class="main-container">
        <img src="~/assets/images/trello_logo.png" class="logo" alt="trello logo"/>
        <h1>Connectez-vous pour continuer</h1>
        <GoogleSignInButton
            @success="handleLoginSuccess"
            @error="handleLoginError"
            ></GoogleSignInButton>
    </UContainer>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useAuthStore } from '~/store/auth';
import { GoogleSignInButton, type CredentialResponse} from "vue3-google-signin";


const { authenticateUser } = useAuthStore();
const { authenticated } = storeToRefs(useAuthStore());
const router = useRouter();

// handle success event
const handleLoginSuccess = async (response: CredentialResponse) => {
    const { credential } = response;
    const login = async() => {
        try {
            const response = await fetch(`http://0.0.0.0:5080/user/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + credential
                },
            });
            if (!response.ok) {
                const errBody = await response.json();
                throw { status: response.status, body: errBody};
            }
            return await response.json();
        } catch (err) {
            console.error('Network / fetch error login', err);
            throw err;
        }
    }
    const loginResult = await login();
    console.log(`this is loginresult ${loginResult}`);

    authenticateUser(credential);
    if (authenticated) {
        router.push('/');
    }
};

// handle an error event
const handleLoginError = () => {
  console.error("Login failed");
};
</script>

<style>
.main-container {
    width: fit-content;
    margin-top: 6%;
    padding: 2%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: var(--secondary-grey);
    gap: 30px;
    box-shadow: 0px 0px 25px 0px rgba(0,0,0,0.65);
}

.logo {
    height: 40px;
}
</style>
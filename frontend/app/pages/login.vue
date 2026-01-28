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

const { $bridge } = useNuxtApp()
const api = $bridge;
const { authenticateUser } = useAuthStore();
const { authenticated } = storeToRefs(useAuthStore());
const router = useRouter();
const toast = useToast()

const handleLoginSuccess = async (response: CredentialResponse) => {
    const { credential } = response;
    const data = await api.login(credential).catch((error) => {
        console.error(error);
        toast.add({
            title: 'Error',
            description: 'Failed to login.',
            color: 'error',
            ui: {
                root: 'bg-[var(--secondary-grey)]',
            },
            })
    });

    if (data) {
        authenticateUser(credential, data);
        if (authenticated) {
            router.push('/');
        }
    }
};

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
<script>
    import { store } from "../hooks/auth";


    async function logout() {
        $store.username = null;
    }
</script>

<button on:click={logout}>Logout</button>
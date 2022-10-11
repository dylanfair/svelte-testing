<script>
    import { store } from "../hooks/auth";


    async function logout() {
        $store = null;
    }
</script>

<button on:click={logout}>Logout</button>
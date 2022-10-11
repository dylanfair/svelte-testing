<script>
  import Login from './lib/Login.svelte';
  import Welcome from './lib/Welcome.svelte';
  import Logout from './lib/Logout.svelte';
  import Todos from './lib/Todos.svelte';
  import { store } from './hooks/auth';
</script>

<main>
  {#if $store != null }
    <Todos />
    <Logout />
  {:else}
    <Welcome />
    <Login />
  {/if}
</main>



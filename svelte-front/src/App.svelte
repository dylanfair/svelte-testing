<script>
  import Welcome from './lib/Welcome.svelte';
  import Login from './lib/Login.svelte';
  import Logout from './lib/Logout.svelte';
  import Signup from './lib/Signup.svelte';
  
  import Todos from './lib/Todos.svelte';
  import { store } from './hooks/auth';

  let signupLogic = 0;

  async function signupShow() {
    signupLogic = 1;
  }
  async function returnToLogin() {
    signupLogic = 0;
  }
</script>

<main>
  {#if $store.username != null }
    <Todos />
    <Logout />
  {:else if signupLogic == 1}
    <Welcome />
    <Signup />
    <br>
    <button on:click|preventDefault={returnToLogin} class="ui blue button">Already have an account?</button>
  {:else}
    <Welcome />
    <Login />
    <p>Or click below to register</p>
    <button on:click|preventDefault={signupShow} class="ui blue button">Register</button>
  {/if}
</main>



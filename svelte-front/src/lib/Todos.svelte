<script>
    import { store } from "../hooks/auth";
    import { onMount } from "svelte";

    export let todos_list = [];

    // Query database for Todos given the user which is in 'store'
    async function fetch_todos(){
        const todos_response = await fetch(`http://localhost:8080/${$store}/todos`, {
            headers: {"username": `${$store}`}
            // credentials: 'include',
        });
        const data = await todos_response.text();
        console.log(data);
        var array = JSON.parse("[" + data + "]")
        console.log(array)
        todos_list = array[0];
    }
    onMount(fetch_todos)
    
</script>

<p>Welcome {$store}</p>

<ul>
    {#each todos_list as { todo, complete} }
        <li>{todo} - {complete}</li>
    {/each}
</ul>
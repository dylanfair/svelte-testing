<script>
    import { store } from "../hooks/auth";

    let text = 'Login below to check your todo list!';
    // send data to backend API?
    let username = '';
    let password = '';

    async function login() {        
        const res = await fetch("http://localhost:8080/token", {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        console.log(res)

        // Do I want the response to just be a true or false to keep things simple?
        const success = await res.json()
        console.log(success)

        if (success.message == true) {
            $store.username = `${username}`
            $store.password = `${password}`
        } else {
            text = "Incorrect, try again"
        }
        
    }
</script>

<main>
    <p>{text}</p>

    <form on:submit|preventDefault={login} class="ui login-form">
                    
        <label for="username">Username</label>
        
        <div class="field">
            <input type="text" required name="username" placeholder="Username" bind:value={username}>
            <br>
        </div>
        <label for="password">Password</label>
        <div class="field">
            <input type="password" required name="password" placeholder="Password" bind:value={password}>
            <br>
        </div>
        <br>
        <button class="ui blue form-button" type="submit">Login</button>
    </form>
</main>

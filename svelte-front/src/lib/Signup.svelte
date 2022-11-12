<script>
    import { store } from "../hooks/auth";

    let text = 'Or click below to signup';
    // send data to backend API?
    let username = '';
    let password = '';

    async function signup() {        
        const res = await fetch("http://localhost:8080/signup", {
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
            text = "That account already exists?"
        }
        
    }
</script>

<main>
    <form on:submit|preventDefault={signup} class="ui login-form">
                    
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
        <button class="ui blue form-button" type="submit">Signup</button>
    </form>
</main>

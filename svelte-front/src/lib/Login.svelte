<script>
    let text = '0';
    // send data to backend API?
    let username = '';
    let password = '';
    let result = null;

    async function login() {        
        const res = await fetch("http://localhost:8080/token", {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        console.log(res)

        // fetch("http://localhost:8080/success")
        //     .then(d => d.text())
        //     .then(d => (text = d))
        // Do I want the response to just be a true or false to keep things simple?
        const success = await res.text()
        console.log(success)
        // result = JSON.stringify(json)
        if (success === '"Success!"') {
            text = "You are logged in!"
        } else {
            text = "Incorrect, try again"
        }
        
    }
</script>

<main>
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
    
    <p>{text}</p>
</main>

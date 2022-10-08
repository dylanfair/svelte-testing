<script type="javascript">
	let rand = "-1";

    function getRand() {
        fetch("https://svelte-testing-nddqi3no6a-uc.a.run.app/rand")
        .then(d => d.text())
        .then(d => (rand = d));
    }

</script>

<main>
	<h1>Hello {rand}!</h1>
	<button on:click={getRand}>Get a random number</button>
</main>
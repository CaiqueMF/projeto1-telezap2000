<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import { goto } from '$app/navigation';

    let pesquisa = ''
    let salas = []
    let resultados = [] 

    onMount(async () => {
        await fetchSalas();
    });
  

    async function fetchSalas() {
        try {
            const response = await axios.get(`http://localhost:5000/api/salas`);
            salas = response.data;
            resultados = salas
        } catch (error) {
            console.error(error);
        }
    }
</script>

<main>
    <div class='busca'>
        <h1>Venha <span>organizar</span> os seus horários</h1>
        <h3>Conte com a ajuda da Fada para visualizar as disponibilidades das salas agora e durante a semana</h3>
        <input type="text" placeholder="🔍︎" bind:value={pesquisa}>
        {#each resultados as resultado}
            {#if resultado.nome.toLowerCase().includes(pesquisa.toLowerCase()) && !pesquisa == ''}
                <button class="resultado" on:click={goto(`sala/${resultado.id}`)}>{resultado.nome}</button>
            {/if}
        {/each}
    </div>
    <div class="fada">
        <img src="fada1.png" alt="Fada">
    </div>
</main>

<style>
    main {
        height: 100vh;
        display: flex;
        justify-content: space-evenly;
        color: black;
        background-image:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),  url('Iurifoto1.png');
        background-size: cover;
        background-position: center;
    }

    h1 {
        font-family: 'Playfair Display', Times, serif;
        font-size: 90px;
        font-weight: 400;
        padding-top: 10%;
    }

    h3 {
        font-family: 'Outfit', sans-serif;
        padding-bottom: 10%;
    }

    span {
        color: #244E2C;
    }

    input {
        width: 100%;
        background: #BC4749;
        border-radius: 30px;
        border-style: none;
        height: 5vh;
        padding-left: 3%;
        box-shadow: inset 0 1px 2px rgba(0,0,0,.39), 0 -1px 1px rgba(0,0,0,.39), 0 1px 0 rgba(0,0,0,.39);
    }

    input::placeholder {
        position: relative;
        top: 3%;
        padding-left: 93%;
        font-size: x-large;
        color: white;
    }

    .resultado {
        width: 100%;
        padding: 5px;
        border: 1px black solid;
        background-color: white;
    }

    .resultado:hover {
        background-color: #D6D6D6;
    }

    .busca {
        margin-left: 10%;
        width: 33%;
    }

    .fada {
        margin-right: 10%;
    }
</style>

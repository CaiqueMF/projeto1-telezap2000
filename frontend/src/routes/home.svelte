<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let pesquisa = ''
    let cadeiras = []
    let salas = []
    let resultados = [] 

    onMount(async () => {
        await fetchCadeiras();
        await fetchSalas();
    });
  
    async function fetchCadeiras() {
        try {
            const response = await axios.get('http://localhost:5000/api/cadeiras');
            cadeiras = response.data;
            resultados = [...resultados, ...cadeiras];
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchSalas() {
        try {
            const response = await axios.get(`http://localhost:5000/api/salas`);
            salas = response.data;
            resultados = [...resultados, ...salas];
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
            {#if resultado.nome.toLowerCase().includes(pesquisa.toLowerCase())}
                <div class="resultado">{resultado.nome}</div>
            {/if}
        {/each}
    </div>
    <div class="fada">
    <img src="fada.jpg" alt="Fada">
    </div>
</main>

<style>
    main {
        display: flex;
        align-items: center;
        justify-content: space-evenly;
        color: black;
    }

    h1 {
        font-family: 'Times New Roman', Times, serif;
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
        box-shadow: inset 0 1px 2px rgba(0,0,0,.39), 0 -1px 1px #FFF, 0 1px 0 #FFF;
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
    }

    .busca {
        margin-left: 10%;
        width: 33%;
    }

    .fada {
        margin-right: 10%;
    }
</style>

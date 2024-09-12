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
            resultados = [...resultados, ...cadeiras];  // Adiciona as cadeiras ao array de resultados
        } catch (error) {
            console.error(error);
        }
    }

    async function fetchSalas() {
        try {
            const response = await axios.get(`http://localhost:5000/api/salas`);
            salas = response.data;
            resultados = [...resultados, ...salas];  // Adiciona as salas ao array de resultados
        } catch (error) {
            console.error(error);
        }
    }
</script>

<main>
  <h1>Organize seus <span>Horários</span></h1>
  <h3>Conte com a ajuda da <span>Fada</span> para buscar e organizar suas disciplinas</h3>
  
  <input type="text" placeholder="🔍︎" bind:value={pesquisa}>
  
  {#each resultados as resultado}
    {#if resultado.nome.toLowerCase().includes(pesquisa.toLowerCase())}
        <div class="resultado">{resultado.nome}</div>
    {/if}
  {/each}
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        color: black;
    }

    h1 {
        font-family: 'Times New Roman', Times, serif;
        font-size: 90px;
        font-weight: 400;
        padding-top: 10%;
    }

    h3 {
        font-family: 'Marvel', sans-serif;
        padding: 10% 0;
    }

    span {
        color: #5A7302;
    }

    input {
        width: 100%;
        background: #5A7302;
        border-radius: 20px;
        border-style: none;
        height: 5vh;
        padding-left: 3%;
    }

    input::placeholder {
       padding-left: 97%;
       color: black;
    }

    .resultado {
        width: 100%;
        padding: 5px;
        border: 1px black solid;
    }
</style>

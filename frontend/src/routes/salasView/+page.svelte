<script>
    import { onMount } from 'svelte';
    import axios from 'axios';

    let salas = []

    onMount(async () => {
        await fetchSalas();
    });

    async function fetchSalas() {
        try {
            const response = await axios.get(`http://localhost:5000/api/salas`);
            salas = response.data;
            console.log(salas);
        } catch (error) {
            console.error(error);
        }
    }
</script>

<main>
    <div class="square">
        <div>
            <h1>Laboratórios - 1º e 2º andar</h1>
            <div class="salas">
                {#each salas as sala (sala.id)}
                    {#if sala.tipos == "Laboratório básico" || sala.tipos == "Laboratório avançado"}
                        <div class="salaSquare">
                            <div class="content">
                                <p>{sala.nome}</p>
                                {#if sala.tipos == "Laboratório básico"}
                                    <p class="tipo">Computadores Dell</p>
                                {:else}
                                    <p class="tipo">Computadores Mac</p>
                                {/if}
                            </div>
                            <a href={`../sala/${sala.id}`}><i class="fa fa-chevron-right" aria-hidden="true"></i></a>
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
        <div>
            <h1>Salas - Térreo</h1>
            <div class="salas">
                {#each salas as sala (sala.id)}
                    {#if sala.tipos == "Sala normal" || sala.tipos == "Sala grande" || sala.tipos == "Ateliê"}
                        <div class="salaSquare">
                            <div class="content">
                                <p>{sala.nome}</p>
                                {#if sala.tipos == "Sala normal" || sala.tipos == "Ateliê"}
                                    <p class="tipo">Para 30 alunos</p>
                                {:else}
                                    <p class="tipo">Para 60 alunos</p>
                                {/if}
                            </div>
                            <a href={`../sala/${sala.id}`}><i class="fa fa-chevron-right" aria-hidden="true"></i></a>
                        </div>
                    {/if}
                {/each}
            </div>
        </div>
    </div>
</main>

<style>
    main {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    h1 {
        font-family: "Playfair Display";
        font-weight: 400;
        color: black;
        padding: 10px;
        padding-bottom: 30px;
    }

    .square {
        border: 1px solid black;
        padding: 15px;
        border-radius: 20px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 90%;
        height: 80%;
        margin-top: 5%;
        background-color: white;
    }

    .square div {
        width: 100%;
    }

    .salas {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px; 
        width: 100%;
        justify-items: center; 
    }

    .salaSquare {
        color: white;
        background-color: #244E2C;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
        padding: 10px;
        height: 100px; 
        text-align: left; 
        justify-content: space-between; 
        align-items: flex-start; 
        position: relative; 
    }

    .salaSquare .content {
        flex: 1;
    }

    .salaSquare i {
        color: white;
        position: absolute;
        bottom: 10px;
        right: 10px;
        font-size: 16px;
    }

    .salaSquare p {
        margin: 0;
        font-weight: 400;
    }

    .tipo {
        font-size: 1rem;
    }
    </style>

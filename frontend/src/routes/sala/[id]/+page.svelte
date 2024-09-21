<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import { goto } from '$app/navigation';
    import '@fortawesome/fontawesome-free/css/all.min.css'

    let sala = '';
    let id = '';

    $: id = String($page.params.id);

    let salas = [];

    onMount(async () => {
        await fetchSalas();
        findSalaById(id);
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

    function findSalaById(id) {
        console.log("ID recebido:", id);
        const salaEncontrada = salas.find(sala => String(sala.id) === id);
        if (salaEncontrada) {
            sala = salaEncontrada.nome; 
        } else {
            console.error('Sala não encontrada');
        }
    }
</script>

<main>
    <div class="info">
        <i class="fa-solid fa-arrow-left"></i>
        <p>{sala}</p>
        <p>Horários disponíveis</p>
        <p>Aulas</p>
    </div>
    <div class="horarios">
        <table>
            <tr>
                <th>Segunda-feira</th>
                <th>Terça-feira</th>
                <th>Quarta-feira</th>
                <th>Quinta-feira</th>
                <th>Sexta-feira</th>
            </tr>
            {#each {length: 6} as _, i} 
            <tr>
                <td>08:00 até as 10:00</td>
                <td>08:00 até as 10:00</td>
                <td>08:00 até as 10:00</td>
                <td>08:00 até as 10:00</td>
                <td>08:00 até as 10:00</td>
                <td>08:00 até as 10:00</td>
            </tr>
            {/each}
        </table>
    </div>
</main>

<style>
    i {
        color: black;
    }

    main {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .info {
        border: 1px black solid;
        width: 80%;
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-top: 3%;
        padding: 0.3%;
        gap: 10px;
    }

    table {
        width: 80%;
        border-collapse: collapse;
        margin-top: 2%;
    }

    th, td {
        border: 1px solid black;
        text-align: center;
        padding: 8px;
    }

    th {
        background-color: #f2f2f2;
    }

    td {
        height: 50px;
    }
</style>
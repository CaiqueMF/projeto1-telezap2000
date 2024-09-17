<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
	import { token, user } from '../../store';

	$: currentUser = $user.username;
    let id_professor = ''; // Captura do id do professor logado

    let cadeiras = [];
    let professores = [];
    let salas = [];
    let turmas = [];

    let feedback = '';
    let feedbackSuccess = ''; // Mensagem de sucesso no envio do feedback
    let feedbackError = ''; // Mensagem de erro no envio do feedback

    onMount(async () => {
        await fetchOptions();
        await fetchTurmas();
    });

    async function fetchOptions() {
        try {
            const [cadeiraRes, professorRes, salaRes] = await Promise.all([
                axios.get('http://localhost:5000/api/cadeiras'),
                axios.get('http://localhost:5000/api/professores'),
                axios.get('http://localhost:5000/api/salas')
            ]);

            cadeiras = cadeiraRes.data;
            professores = professorRes.data;
            salas = salaRes.data;

            $: id_professor = professores.find(p => p.nome === currentUser)?.id || '';
        } catch (error) {
            console.error('Erro ao carregar opções:', error);
        }
    }

    async function addFeedback() {
        if (!feedback) {
            feedbackError = 'O feedback não pode estar vazio.';
            return;
        }

        try {
            const newFeedback = {
                id_professor,
                feedback
            };
            await axios.post('http://localhost:5000/api/feedbacks', newFeedback);
            feedback = ''; // Limpar o campo de feedback após o envio
            feedbackSuccess = 'Feedback enviado com sucesso!';
            feedbackError = ''; // Limpar a mensagem de erro
        } catch (error) {
            feedbackError = 'Erro ao enviar feedback. Tente novamente.';
            console.error('Erro ao enviar feedback:', error);
        }
    }

    async function fetchTurmas() {
        try {
            const response = await axios.get('http://localhost:5000/api/turmas');
            turmas = await Promise.all(response.data.map(async turma => {
                // Buscar os nomes com base nos IDs
                const cadeira = cadeiras.find(c => c.id === turma.id_cadeira);
                const professor = professores.find(p => p.id === turma.id_professor);
                const sala = salas.find(s => s.id === turma.id_sala);

                return {
                    ...turma,
                    nome_cadeira: cadeira ? cadeira.nome : 'Desconhecido',
                    nome_professor: professor ? professor.nome : 'Desconhecido',
                    nome_sala: sala ? sala.nome : 'Desconhecido'
                };
            }));
        } catch (error) {
            console.error('Erro ao carregar turmas:', error);
        }
    }
</script>

<main>
    <h1>Minhas Turmas</h1>
    <div id="turmas">
        {#each turmas as turma}
            {#if turma.id_professor == id_professor}
                <div class="turma">
                    <p class="nome_disciplina">{turma.nome_cadeira} T{turma.n_turma}</p>
                    <p class="nome_sala">{turma.nome_sala}</p>
                </div>
            {/if}
        {/each}
    </div>

    <div id="feedback">
        <h2>Enviar feedback</h2>
        <p>Envie alguma sugestão para os coordenadores de como melhorar os horários das suas disciplinas</p>
        
        {#if feedbackSuccess}
            <p class="success">{feedbackSuccess}</p>
        {/if}

        {#if feedbackError}
            <p class="error">{feedbackError}</p>
        {/if}

        <form on:submit|preventDefault={addFeedback}>
            <input bind:value={feedback} placeholder="Escreva aqui seu feedback">
            <button type='submit'>Enviar Feedback</button>
        </form>
    </div>
</main>

<style>
    main {
        display: flex;
        flex-direction: column;
    }

    h1, h2 {
        font-family: 'Times New Roman', Times, serif;
    }

    #turmas {
        display: flex;
        gap: 5%;
    }

    .turma {
        background-color: #5A7302;
        color: white;
        width: 33%;
        border-radius: 10px;
        padding: 10px;
    }

    input {
        width: 100%;
        height: 100px;
        padding: 10px;
        font-size: 1em;
        margin-bottom: 10px;
        border-style: none;
        background-color: #D9D9D9;
        border-radius: 20px;
    }

    input::placeholder {
       position: relative;
       color: #505050;
       bottom: 30px
    }
    
    .success {
        color: green;
        margin-bottom: 10px;
    }

    .error {
        color: red;
        margin-bottom: 10px;
    }

    button {
        padding: 10px 30px;
        color: white;
        background-color: #0468BF;
        border-style: none;
        border-radius: 20px;
    }
</style>

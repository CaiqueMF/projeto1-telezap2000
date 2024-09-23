<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import { goto } from '$app/navigation';
	import { token, user } from '../../store';

	$: currentUser = $user.id_professor;
    $: currentName = $user.nome;

    let currentUsername = $user.username;
    let senha = ''
    let cadeiras = [];
    let professores = [];
    let salas = [];
    let turmas = [];
    let alocacoes = []

    let dicionario_dia = {
      "1":"Segunda feira",
      "2":"Terça feira",
      "3":"Quarta feira",
      "4":"Quinta feira",
      "5":"Sexta feira",
      "6":"Sábado",
    }
    let feedback = '';
    let feedbackSuccess = ''; // Mensagem de sucesso no envio do feedback
    let feedbackError = ''; // Mensagem de erro no envio do feedback

    onMount(async () => {
        await fetchOptions();
        await fetchTurmas();
        await fetchAlocacoes();
        const currentUser = $user;
        if (!currentUser.isAuthenticated) {
           goto('/');
        }
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
                currentUser,
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

    async function fetchAlocacoes() {
        try {
            const response = await axios.get('http://localhost:5000/api/alocacoes');
            alocacoes = response.data;
            turmas = turmas.map(turma => {
                const alocacoesDaTurma = alocacoes.filter(alocacao => alocacao.id_turma === turma.id);
                return {
                    ...turma,
                    alocacoes: alocacoesDaTurma.length > 0 ? alocacoesDaTurma : [] // Se não houver alocações, mantém o array vazio
                };
            });
        } catch (error) {
            console.error('Erro ao carregar alocações:', error);
        }
    }

    async function atualizarLogin() {
        try{
            const response = await axios.put(`http://localhost:5000/api/update_login`,{

                login_novo: currentUsername,
                login_antigo: $user.username,
            })
            console.log(response.data.message)
        }catch(error){
            console.error('erro ao atualizar login:', error.response.data.message)
        }
    }

    async function atualizarSenha() {
        try{
            const response = await axios.put(`http://localhost:5000/api/update_password`,{
                senha: senha,
                login: $user.username,
            })
            console.log(response.data.message)
            senha = ''
        }catch(error){
            console.error('erro ao atualizar senha:', error.response.data.message)
        }
    }
</script>

<main>
    <div class="content">
        <div id="turmas">
            <h1>Minhas Disciplinas</h1>
            <p>Aqui estão todas as suas disciplinas</p>
            <div class="gridCointainer">
                {#each turmas as turma}
                {#if turma.id_professor == currentUser}
                    <div class="turma">
                        <p class="nome_disciplina">{turma.nome_cadeira} T{turma.n_turma}</p>
                        <p class="nome_sala">{turma.nome_sala}</p>
                        {#if turma.alocacoes && turma.alocacoes.length > 0}
                            {#each turma.alocacoes as alocacao}
                                <p>{dicionario_dia[alocacao.dia]} - {alocacao.horario}:00 à {alocacao.horario+alocacao.duracao}:00</p>
                            {/each}
                        {/if}
                    </div>
                {/if}
            {/each}
            </div> 
        </div>
        <div class="horizontal">
            <div id="feedback">
                <h2>Enviar feedback</h2>
                <p>Envie alguma sugestão para os coordenadores de como melhorar os horários da suas disciplinas</p>
                
                {#if feedbackSuccess}
                    <p class="success">{feedbackSuccess}</p>
                {/if}
        
                {#if feedbackError}
                    <p class="error">{feedbackError}</p>
                {/if}
        
                <form on:submit|preventDefault={addFeedback}>
                    <textarea
                    class="feedbackInput"
                    bind:value={feedback}
                    placeholder="Escreva aqui seu feedback"
                    ></textarea>
                    <button class="feedbackButton" type='submit'>Enviar Feedback</button>
                </form>
            </div>
        
            <div id="conta">
                <h2>Conta</h2>
                <p>Aqui estão todos os dados da sua conta no Fada</p>
                <div class="nomeProfessor">
                    <img src="account_circle.png" alt="ícone perfil">
                    <p>{currentName}</p>
                </div>
                <div class="horizontal">
                    <div class="usuarioESenha">
                        <div>
                            <p>Usuário</p>
                            <button on:click={()=>{atualizarLogin()}}><img src="pen.png" alt="atulizar usuário"></button>
                        </div>
                        <input bind:value={currentUsername}>
                    </div>
                    <div class="usuarioESenha">
                        <div>
                            <p>Senha</p>
                            <button on:click={()=>{atualizarSenha()}}><img src="pen.png" alt="atualizar senha"></button>
                        </div>
                        <input type="password" bind:value={senha} placeholder={senha}>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

<style>
    .usuarioESenha {
        width: 50%;
        background-color: #D9D9D9;
        height: 120px;
        padding: 10px;
        
    }
    .usuarioESenha div{
        display: flex;
        justify-content: space-between;
        
    }
    .usuarioESenha p{
        font-family: "Outfit";
        font-size: 18px;
        font-weight: 600;
    }
    .usuarioESenha button{
        background-color: transparent;
        border: none;
        cursor: pointer;
    }
    .usuarioESenha input{
        background-color: transparent;
        border: none;
        font-family: "Outfit";
        font-size: 16px;
        width: 100%;
        height: 60%;
    }
    .nomeProfessor {
        display: flex;
        align-items: center;
        background-color: #D9D9D9;
        height: 88px;
        padding: 10px;
        margin-top: 15px;
        gap: 15px;
    }
    .nomeProfessor p{
        font-family: "Outfit";
        font-size: 26px;
        font-weight: 600;
    }
    .content {
        width: 80vw;
        margin: auto;
        padding-top: 10vh;
    }
    .content div{
        border-radius: 20px;
    }
    main{
        background-image:linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),  url('Iurifoto5 1.png');
        height: 95vh;
        background-size: cover;
        background-position: center;
    }
    h1 {
        font-family: "Playfair Display";
        height: 42px;
    }
    h2 {
        font-family: "Playfair Display";
        height: 28px;
    }
    p {
        font-family: "Outfit";
        font-size: 16px;
        margin-bottom: 10px;
    }
    .horizontal{
        display: flex;
        gap: 15px;
        width: 100%;
        margin-top: 15px;
    }
    .gridCointainer{
        display: grid;
        grid-template-columns: repeat(3,1fr);
        gap: 20px;
    }
    .turma {
        background-color: rgb(217, 217, 217);
        margin-top: 10px;
        padding: 10px;
    }
    #turmas {
        padding: 10px;
        background-color: white;
    }
    #feedback {
        padding: 10px;
        background-color: white;
        width: 50%;
        padding: 20px; /* Aumenta a área clicável do textarea */
    }
    #conta {
        padding: 20px;
        background-color: white;
        width: 50%;
    }
    form {
        margin-top: 10px;
        display: flex;
        flex-direction: column;
        align-items: end;
        gap: 5px;
    }
    .feedbackInput {
        width: 100%;
        height: 200px;
        padding: 10px;
        margin-top: 5px;
        font-size: 16px; /* Define o tamanho da fonte */
        border-radius: 20px; /* Bordas arredondadas */
        background-color: #D9D9D9; /* Define a cor cinza */
        resize: none; /* Impede que o usuário redimensione o textarea */
        border: none;
    }
    .feedbackButton {
        background-color: #BC4749;
        border: none;
        width: 180px;
        height: 35px;
        border-radius: 15px;
        font-family: "Outfit";
        color: white;
    }
</style>
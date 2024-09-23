<script>
    import { onMount } from 'svelte';
    import axios from 'axios';
    import NavigationCoordenador from '../navigationCoordenador.svelte';
    import { goto } from '$app/navigation';
    import { token, user } from '../../store';
    
    let feedbacks = [];
    let professores = [];
    
    onMount(async () => {
      await fetchData();
      const currentUser = $user;
      if (!currentUser.isAuthenticated) {
        goto('/');
      }
    });
  
    // Função que busca feedbacks e professores
    async function fetchData() {
      try {
        const feedbacksResponse = await axios.get(`http://localhost:5000/api/feedbacks`);
        feedbacks = feedbacksResponse.data;
  
        const professoresResponse = await axios.get(`http://localhost:5000/api/professores`);
        professores = professoresResponse.data;
  
        console.log(feedbacks, professores);
      } catch (error) {
        console.error(error);
      }
    }
  
    // Função que retorna o nome do professor pelo ID
    function getProfessorName(id_professor) {
      if (professores.length === 0) {
        return 'Desconhecido'; // Garante que a função não falha enquanto `professores` não é carregado
      }
      const professor = professores.find(prof => prof.id === id_professor);
      return professor ? professor.nome : 'Desconhecido';
    }
  </script>
  
  <main>
    <NavigationCoordenador />
    <div class="feedbacks">
      <h1>Feedbacks</h1>
      <p>Aqui estão todos os feedbacks recebidos pelos professores</p>
    </div>
    <div class="listaFeedbacks">
      {#if feedbacks.length > 0 && professores.length > 0}
        {#each feedbacks as feedback}
          <div class="feedback">
            <div class="userLine">
                <i class="fa-regular fa-circle-user"></i>
                <h2>{getProfessorName(feedback.id_professor)}</h2>
            </div>
            <p>{feedback.feedback}</p>
          </div>
        {/each}
      {/if}
    </div>
  </main>
  <style>
    main {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 0 10%;
      font-family: 'Outfit';
      font-weight: 400;
      background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('Iurifoto5 1.png');
      height: 100vh;
      background-size: cover;
      background-position: center;
    }
  
    h1 {
      font-family: "Playfair Display";
      font-size: 42px;
    }
  
    .feedbacks {
      display: flex;
      flex-direction: column;
      width: 100%;
      background-color: white;
      border-radius: 20px;
      margin-top: 3%;
      padding: 10px;
    }
  
    .listaFeedbacks {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 10px;
      width: 100%;
      margin-top: 20px;
    }
  
    .feedback {
      background-color: #D9D9D9;
      border-radius: 10px;
      padding: 20px;
    }
  
    .feedback h2 {
      font-size: 18px;
      font-weight: bold;
      padding-left: 10px;
    }
  
    .feedback p {
      font-size: 16px;
    }

    .userLine {
        display: flex;
        align-items: center;
    }

    i {
        font-size: 18px;
        color: black;
    }
  </style>
  
<script>
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';
  import { token, user } from '../store';

</script>

<main>
  <h1>Organize seus <span>Horários</span></h1>
  <h3>Conte com a ajuda da <span>Fada</span> para buscar e organizar suas disciplinas</h3>
  <input type="text" placeholder="🔍︎">
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
        font-size: 100px;
        padding-top: 10%;
    }
    h3 {
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
</style>

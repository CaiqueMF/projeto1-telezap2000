<script>
	let currentPath = "";
  
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	// Define a URL atual quando o componente é montado
	onMount(() => {
	  currentPath = window.location.pathname;
	});
  
	function isActive(path) {
		console.log(path)
	  return $page.url.pathname  === path ? 'active' : '';
	}
  </script>
  
  <div class="btns">
	  <button class={isActive('/cadeiras')}><a href="/cadeiras">Disciplinas</a></button>
	  <button class={isActive('/turmas')}><a href="/turmas">Turmas</a></button>
	  <button class={isActive('/professores')}><a href="/professores">Professores</a></button>
	  <button class={isActive('/salas')}><a href="/salas">Salas</a></button>
	  <button class={isActive('/feedbacks')}><a href="/feedbacks">Feedbacks</a></button>
  </div>
  
  <style>
	  .btns {
		  display: flex;
		  align-items: center;
		  width: 100%;
		  background-color: white;
		  border-radius: 20px;
		  margin-top: 3%;
		  flex-direction: row;
		  padding: 0.3%;
		  gap: 20px;
		  padding: 10px;
	  }
  
	  button {
		  border: none;
		  background: none;
		  font-size: 16px;
	  }
  
	  .btns button:hover {
		  font-weight: 700;
	  }
  
	  a {
		  color: #BC4749;
		  text-decoration: none;
	  }
  
	  .active a {
		  font-weight: bold;
	  }
  </style>
  
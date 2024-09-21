<script> 
	import { page } from '$app/stores';
	import { token, user } from '../store';
	import '@fortawesome/fontawesome-free/css/all.min.css'

	$: currentUser = $user.role;
</script>
<link href="https://fonts.googleapis.com/css2?family=Moon+Dance&display=swap" rel="stylesheet">
<header>
	<nav>
		<ul>
			<li>
				<p>Fada</p>
			</li>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined} class="home">
				<a href="/">Home</a>
			</li>
			<li aria-current={$page.url.pathname === '/agora' ? 'page' : undefined} class="agora">
				<a href="/agora">Agora</a>
			</li>
			<li aria-current={$page.url.pathname === '/salasView' ? 'page' : undefined} class="salas">
				<a href="/salasView">Salas</a>
			</li>
			{#if currentUser == "user"}
			<li aria-current={$page.url.pathname === '/professor' ? 'page' : undefined}>
				<a href="/professor">Professor</a>
			</li>
			{/if}
			{#if currentUser == null}
			<li aria-current={$page.url.pathname === '/login' ? 'page' : undefined} class="login">
				<a href="/login">Login Administrador</a> <i class="fa-regular fa-circle-user"></i>
			</li>
			{/if}
		</ul>
	</nav>
</header>

<style>

header {
	background: #244E2C;
	height: 5vh;
}

nav {
	background: #244E2C;
	height: 100%;
	display: flex;
	align-items: center;
}

ul {
	padding: 0;
	margin: 0;
	list-style: none;
	display: flex; 
	width: 100%; 
	height: 100%;
}

li {
	display: flex;
	align-items: center;
	padding: 0 1rem;
	height: 100%;
}

ul li p {
	color: white;
	font-family: "Moon Dance", cursive;
	font-size: 2rem;
	font-weight: 400;
}

li[aria-current='page'] a {
	font-weight: 600;
}

nav a {
	display: flex;
	align-items: center;
	height: 100%;
	color: white;
	font-size: 1rem;
	letter-spacing: 0.1em;
	transition: color 0.2s linear;
	font-family: "Outfit";
}

.login {
	margin-left: auto;
}

.home {
	padding-left: 2%;
}

i {
	padding-left: 10px;
}
</style>

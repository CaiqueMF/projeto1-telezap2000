<script>
	import { page } from '$app/stores';
	import { token, user } from '../store';

	$: currentUser = $user.role;

	console.log(currentUser);
</script>

<header>
	<nav>
		<ul>
			<li aria-current={$page.url.pathname === '/' ? 'page' : undefined}>
				<a href="/">Home</a>
			</li>
			{#if currentUser == "user"}
			<li aria-current={$page.url.pathname === '/professor' ? 'page' : undefined}>
				<a href="/professor">Professor</a>
			</li>
			{/if}
			<li aria-current={$page.url.pathname === '/agora' ? 'page' : undefined}>
				<a href="/agora">Agora</a>
			</li>
			{#if currentUser == "admin"}
			<li aria-current={$page.url.pathname === '/cadeiras' ? 'page' : undefined}>
				<a href="/cadeiras">Cadeiras</a>
			</li>
			<li aria-current={$page.url.pathname === '/professores' ? 'page' : undefined}>
				<a href="/professores">Professores</a>
			</li>
			<li aria-current={$page.url.pathname === '/salas' ? 'page' : undefined}>
				<a href="/salas">Salas</a>
			</li>
			<li aria-current={$page.url.pathname === '/turmas' ? 'page' : undefined}>
				<a href="/turmas">Turmas</a>
			</li>
			{/if}
			<li aria-current={$page.url.pathname === '/login' ? 'page' : undefined}>
				<a href="/login">Login</a>
			</li>
		</ul>
	</nav>
</header>

<style>
	header {
		display: flex;
		width: 100%;
		justify-content: center;
		background: #5A7302;
		border-bottom-left-radius: 10px;
		border-bottom-right-radius: 10px;
	}

	nav {
		display: flex;
		justify-items: center;
		justify-content: center;
		background: #5A7302;
	}

	ul {
		padding: 0;
		margin: 0;
		height: 3em;
		display: flex;
		justify-content: center;
		align-items: center;
		list-style: none;
		background-size: contain;
	}

	li {
		padding: 10px;
		height: 100%;
	}

	li[aria-current='page'] a {
		font-weight: 900;
	}

	nav a {
		display: flex;
		height: 100%;
		align-items: center;
		padding: 0 0.5rem;
		color: white;
		font-weight: 700;
		font-size: 0.8rem;
		text-transform: uppercase;
		letter-spacing: 0.1em;
		transition: color 0.2s linear;
	}


</style>

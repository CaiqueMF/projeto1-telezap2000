export { matchers } from './matchers.js';

export const nodes = [
	() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8'),
	() => import('./nodes/9'),
	() => import('./nodes/10'),
	() => import('./nodes/11'),
	() => import('./nodes/12'),
	() => import('./nodes/13'),
	() => import('./nodes/14'),
	() => import('./nodes/15'),
	() => import('./nodes/16'),
	() => import('./nodes/17'),
	() => import('./nodes/18')
];

export const server_loads = [];

export const dictionary = {
		"/": [2],
		"/about": [3],
		"/agora": [4],
		"/cadeiras": [5],
		"/editCadeira/[id]": [6],
		"/editProfessor/[id]": [7],
		"/editSala/[id]": [8],
		"/editTurma/[id]": [9],
		"/login": [10],
		"/planilha": [11],
		"/professores": [13],
		"/professor": [12],
		"/salasView": [15],
		"/salas": [14],
		"/sverdle": [~16],
		"/sverdle/how-to-play": [17],
		"/turmas": [18]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),

	reroute: (() => {})
};

export { default as root } from '../root.svelte';
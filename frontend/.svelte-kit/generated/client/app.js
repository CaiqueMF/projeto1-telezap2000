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
	() => import('./nodes/13')
];

export const server_loads = [];

export const dictionary = {
		"/": [2],
		"/about": [3],
		"/cadeiras": [4],
		"/editCadeira/[id]": [5],
		"/editProfessor/[id]": [6],
		"/editSala/[id]": [7],
		"/editTurma/[id]": [8],
		"/professores": [9],
		"/salas": [10],
		"/sverdle": [~11],
		"/sverdle/how-to-play": [12],
		"/turmas": [13]
	};

export const hooks = {
	handleError: (({ error }) => { console.error(error) }),

	reroute: (() => {})
};

export { default as root } from '../root.svelte';
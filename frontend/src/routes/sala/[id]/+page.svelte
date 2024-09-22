<script>
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import axios from 'axios';
    import '@fortawesome/fontawesome-free/css/all.min.css';

    let sala = '';
    let id = '';
    $: id = String($page.params.id);

    let cadeiras = [];
    let professores = [];
    let salas = [];
    let turmas = [];
    let alocacoes = [];
    
    let horariosPorDia = {
        segunda: [], // Segunda-feira
        terca: [],   // Terça-feira
        quarta: [],  // Quarta-feira
        quinta: [],  // Quinta-feira
        sexta: [],   // Sexta-feira
        sabado: []   // Sábado
    };

    onMount(async () => {
        await fetchOptions();
        await fetchTurmas();
        await fetchAlocacoes();
        findSalaById(id);
        organizeHorarios();
    });

    function findSalaById(id) {
        const salaEncontrada = salas.find(sala => String(sala.id) === id);
        if (salaEncontrada) {
            sala = salaEncontrada.nome; 
        } else {
            console.error('Sala não encontrada');
        }
    }

    function organizeHorarios() {
        turmas.forEach(turma => {
            turma.alocacoes.forEach(alocacao => {
                const dia = alocacao.dia;
                const diaSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado'][dia];

                if (horariosPorDia[diaSemana]) {
                    horariosPorDia[diaSemana].push({
                        turma: turma.nome_cadeira,
                        horario: alocacao.horario,
                        duracao: alocacao.duracao
                    });
                } else {
                    console.warn(`Dia inválido encontrado: ${dia}`);
                }
            });
        });
        horariosPorDia = horariosPorDia
        console.log('Horários organizados:', horariosPorDia);
    }

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

    async function fetchTurmas() {
    try {
        const response = await axios.get('http://localhost:5000/api/turmas');
        turmas = await Promise.all(
            response.data.map(async (turma) => {
                const cadeira = cadeiras.find((c) => c.id === turma.id_cadeira);
                const professor = professores.find((p) => p.id === turma.id_professor);
                const sala = salas.find((s) => s.id === turma.id_sala);

                if (sala && String(sala.id) === id) { // Filtra apenas as turmas da sala atual
                    return {
                        ...turma,
                        nome_cadeira: cadeira ? cadeira.nome : 'Desconhecido',
                        nome_professor: professor ? professor.nome : 'Desconhecido',
                        nome_sala: sala ? sala.nome : 'Desconhecido',
                        alocacoes: []
                    };
                }
            })
        ).then(results => results.filter(turma => turma)); // Remove turmas não filtradas
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
                alocacoes: alocacoesDaTurma
            };
        });
    } catch (error) {
        console.error('Erro ao carregar alocações:', error);
    }
}
</script>

<main>
    <div class="horarios">
        <h1>{sala}</h1>
        <p class="desc">Horários disponíveis</p>
        <table>
    <tr>
        <th>Segunda-feira</th>
        <th>Terça-feira</th>
        <th>Quarta-feira</th>
        <th>Quinta-feira</th>
        <th>Sexa-feira</th>
        <th>Sábado</th>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 8}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 10}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 14}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 16}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 18}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
    <tr>
        <td>
            {#each horariosPorDia.segunda as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.terca as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quarta as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.quinta as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sexta as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
        <td>
            {#each horariosPorDia.sabado as aula}
                {#if aula.horario === 20}
                    <p>{aula.turma}</p>
                    <p>{aula.horario}:00 até as {aula.horario + aula.duracao}:00</p>
                {/if}
            {/each}
        </td>
    </tr>
        </table>
    </div>
</main>

<style>

    main {
        height: 100vh;
        width: 100%;
        display: flex;
        justify-content: center;
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),  url('../Iurifoto3.png');
        background-size: cover;
        background-position: center;
    }
    
    h1 {
        font-family: "Playfair Display";
        font-weight: 400;
        color: black;
        text-align: left;
        align-self: first baseline;
		font-size: 42px;
    }

    .desc {
        align-self: first baseline;
    }

    table {
        width: 100%;
        border-collapse: collapse;
    }

    th, td {
        text-align: center;
        padding: 8px;
        font-family: 'Outfit';
    }

    th {
        font-weight: 700;
        font-size: 20px;
    }

    td {
        height: 50px;
    }

    .horarios {
        padding: 15px;
        border-radius: 20px;
        display: flex;
        align-items: center;
        flex-direction: column;
        width: 90%;
        height: 80%;
        margin-top: 3%;
        background-color: white;
    }
</style>
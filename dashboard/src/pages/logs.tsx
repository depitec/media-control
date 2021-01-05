import { ReactNode, useEffect, useState } from 'react';
// import { logs } from '../../mock/log-data';

function Logs(): ReactNode {
	const [logs, setLogs] = useState<{ control_log: string; server_log: string }>();
	useEffect(() => {
		fetch('/api/logs')
			.then((res) => res.json())
			.then((data) => {
				setLogs(data);
			});
	}, []);

	if (!logs) {
		return <h1>...LOADING</h1>;
	}

	const controlLogLines = logs.control_log.split('\n');
	const controlLogListItems = controlLogLines.map((line, index) => (
		<li className='py-1' key={`control-log-line-${index + 1}`}>
			{line}
		</li>
	));
	const serverLogLines = logs.server_log.split('\n');
	const serverLogListItems = serverLogLines.map((line, index) => (
		<li className='py-1' key={`server-log-line-${index + 1}`}>
			{line}
		</li>
	));
	return (
		<main className='bg-indigo-100 h-screen'>
			<header className='title h-header bg-blue-200 items-center flex justify-center'>
				<h1 className='text-4xl text-center -mt-8'>LOG Files</h1>
			</header>
			<div className='h-content flex flex-row flex-1 justify-evenly mx-8 mb-8 -mt-8 py-4 bg-gray-50 text-sm'>
				{!logs ? undefined : (
					<>
						<div className='flex flex-col'>
							<h2 className='text-xl text-center font-bold pb-2'>Control Log</h2>
							<div className='flex flex-1 overflow-scroll'>
								<ul className='flex flex-col'>{controlLogListItems}</ul>
							</div>
						</div>
						<div className='flex flex-col'>
							<h2 className='text-xl text-center font-bold pb-2'>Server Log</h2>
							<div className='flex flex-1 overflow-scroll'>
								<ul className='flex flex-col'>{serverLogListItems}</ul>
							</div>
						</div>
					</>
				)}
			</div>
		</main>
	);
}

export default Logs;

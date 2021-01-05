import { useEffect, useState } from 'react';
import { Settings, InitalProps } from '@components/Settings';

function IndexPage(): React.ReactNode {
	const [initialProps, setInitialProps] = useState<{ r1: InitalProps; r2: InitalProps }>();
	useEffect(() => {
		fetch(`/api/props`)
			.then((res) => res.json())
			.then((data) => {
				setInitialProps({
					r1: {
						sot: data['sot-1'],
						sct: data['sct-1'],
						name: data['name-1'],
						ip: data['ip-1']
					},
					r2: {
						sot: data['sot-2'],
						sct: data['sct-2'],
						name: data['name-2'],
						ip: data['ip-2']
					}
				});
			});
	}, []);

	return (
		<main className='bg-indigo-100 h-screen'>
			<header className='title h-header bg-blue-200 items-center flex justify-center'>
				<h1 className='text-4xl text-center -mt-8'>Parameter Einstellungen</h1>
			</header>
			<div className='h-content flex flex-row flex-1 justify-evenly mx-16 mb-8 -mt-8 py-4 bg-gray-50 text-sm '>
				{!initialProps ? undefined : (
					<>
						<Settings roomNumber={1} {...initialProps.r1} />
						<Settings roomNumber={2} {...initialProps.r2} />
					</>
				)}
			</div>
		</main>
	);
}

export default IndexPage;

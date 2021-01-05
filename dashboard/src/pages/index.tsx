import { useEffect, useState } from 'react'
import { Settings, InitalProps } from '@components/Settings';

const defaultInitalProps = {
	sot: 0,
	sct: 0,
	ip: '0.0.0.0',
}

function IndexPage(): React.ReactNode {
	const [initialPropsRoom1, setInitialPropsRoom1] = useState<InitalProps>({ ...defaultInitalProps, name: 'Raum 1' });
	const [initialPropsRoom2, setInitialPropsRoom2] = useState<InitalProps>({ ...defaultInitalProps, name: 'Raum 2' });
	useEffect(() => {

		fetch(`/api/props`).then(res => res.json()).then(data => {

			setInitialPropsRoom1({
				sot: data['sot-1'],
				sct: data['sct-1'],
				name: data['name-1'],
				ip: data['ip-1']
			})

			setInitialPropsRoom2({
				sot: data['sot-2'],
				sct: data['sct-2'],
				name: data['name-2'],
				ip: data['ip-2']
			})

		})
	})


	return (
		<main className='bg-indigo-100 h-screen'>
			<div className='title px-6 py-10 bg-blue-200'>
				<h1 className='text-4xl text-center -mt-4'>Raum Parameter Einstellungen</h1>
			</div>
			<div className='flex flex-row justify-evenly items-center mx-8 -mt-4 pb-4 bg-gray-50'>
				<Settings Roomnumber={1} {...initialPropsRoom1} />
				<Settings Roomnumber={2} {...initialPropsRoom2} />
			</div>
		</main>
	);
}

export default IndexPage;

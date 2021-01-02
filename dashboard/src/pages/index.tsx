import { Settings, InitalProps } from '@components/Settings';

function IndexPage(): React.ReactNode {
	const initalSettings = {
		sct: 4,
		sot: 4,
		beamerIP: '200.100.0.22',
		beamerCom: 'PJLINK'
	} as InitalProps;

	return (
		<main className='bg-indigo-100 h-screen'>
			<div className='title px-6 py-10 bg-blue-200'>
				<h1 className='text-4xl text-center -mt-4'>Raum Parameter Einstellungen</h1>
			</div>
			<div className='flex flex-row justify-evenly items-center mx-8 -mt-4 pb-4 bg-gray-50'>
				<Settings Roomnumber={1} subTitle='Klassenraum 312' {...initalSettings} />
				<Settings Roomnumber={2} {...initalSettings} />
			</div>
		</main>
	);
}

export default IndexPage;

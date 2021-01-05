import { useState, ChangeEvent } from 'react';
import { Input } from '@elements/Input';

export interface InitalProps {
	[key: string]: string | number
	sot: number;
	sct: number;
	ip: string;
	// beamerCom: 'ESC/VP21' | 'PJLINK';
	name: string;
}

export interface SettingsProps extends InitalProps {
	Roomnumber: number;
}

export function Settings({ Roomnumber, ...initalProps }: SettingsProps): React.ReactElement {
	const [roomName, setRoomName] = useState(initalProps.name);
	const [sot, setSot] = useState(initalProps.sot);
	const [sct, setSct] = useState(initalProps.sct);
	const [beamerIP, setBeamerIP] = useState(initalProps.ip);
	// const [beamerCOM, setBeamerCOM] = useState(initalProps.beamerCom);

	const H3 = ({ children }: { children: React.ReactNode }): React.ReactElement => {
		return <h3 className='text-xl font-semibold text-center pt-6'>{children}</h3>;
	};

	// const onRadioChange = (value: SettingsProps['beamerCom']) => (): void => {
	// 	setBeamerCOM(value);
	// };

	const onRoomNameChange = (event: ChangeEvent<HTMLInputElement>): void => {
		setRoomName(event.target.value);
	};

	const onTimeChange = (type: 'sot' | 'sct') => (event: ChangeEvent<HTMLInputElement>): void => {
		const { value } = event.target;

		const setFn = type === 'sot' ? setSot : setSct;

		if (Number.isNaN(Number(value))) {
			setFn((v) => v);
			return;
		}

		setFn(Number(event.target.value));
	};

	const onIPChange = (event: ChangeEvent<HTMLInputElement>): void => {
		setBeamerIP(event.target.value);
	};

	const onSave = () => {
		console.log(location.host);
		console.log({ sot, sct, beamerIP, roomName });
	};

	return (
		<div className='settings p-4'>
			<div className='h-16 flex flex-col items-center'>
				<h2 className='settings-headding text-2xl font-bold text-center'>Raum {Roomnumber}</h2>
				<h3 className='text-md text-gray-500 text-center'>
					<input
						value={roomName || ''}
						type='text'
						className='text-md text-center bg-transparent border-b-2 border-gray-100'
						onChange={onRoomNameChange}
						placeholder='Bezeichnung'
					/>
				</h3>
			</div>
			<div className='screen'>
				<div className='section-heading'>
					<H3>Leinwand Einstellungen</H3>
				</div>
				<div className='screen-open-time'>
					<Input
						value={sot}
						type='text'
						label='Zeit zum öffnen [s]'
						onChange={onTimeChange('sot')}
					/>
				</div>
				<div className='screen-close-time'>
					<Input
						value={sct}
						type='text'
						label='Zeit zum schließen [s]'
						onChange={onTimeChange('sct')}
					/>
				</div>
			</div>
			<div className='beamer'>
				<div className='section-heading'>
					<H3>Beamer Einstellungen</H3>
				</div>
				<div className='beamer-ip'>
					<Input value={beamerIP} type='text' label='Beamer IP' onChange={onIPChange} />
				</div>
				{/* <div className='beamer-communication-protocol'>
					<div>
						<Input
							type='radio'
							value='ESC/VP21'
							checked={beamerCOM === 'ESC/VP21'}
							name={`beamer-com-${Roomnumber}`}
							label='ESC/VP21'
							onChange={onRadioChange('ESC/VP21')}
						/>
						<Input
							type='radio'
							value='PJLINK'
							checked={beamerCOM === 'PJLINK'}
							name={`beamer-com-${Roomnumber}`}
							onChange={onRadioChange('PJLINK')}
							label='PJLINK'
						/>
					</div>
				</div> */}
			</div>
			<div className='text-center mt-6'>
				<button className='py-2 px-6 rounded-lg bg-green-400 hover:bg-green-300 ' onClick={onSave}>
					speichern
				</button>
			</div>
		</div>
	);
}

import { InputHTMLAttributes, DetailedHTMLProps } from 'react';

interface InputProps
	extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
	label?: string;
}

export function Input({ label, ...htmlInputProps }: InputProps): React.ReactElement {
	return (
		<div className='flex flex-col p-3'>
			{!label ? undefined : (
				<label className='text-md text-gray-400 text-center pb-2'>{label}</label>
			)}
			<input
				{...htmlInputProps}
				className={
					htmlInputProps.className
						? htmlInputProps.className
						: 'text-xl text-center bg-transparent outline-none focus:ring-2 border-b-2 border-gray-200'
				}
			/>
		</div>
	);
}

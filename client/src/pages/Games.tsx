import { Box, Tab, Tabs} from '@mui/material';
import { useState } from 'react';

// import './Games.module.css'

const Games = () => {
    const [curTab, setCurTab] = useState('Jogos')

    const handleChange = (event: React.SyntheticEvent, newValue: string) => {
        setCurTab(newValue);
      };

    return (
        <Box sx={{ width: '100%', typography: 'body1' }}>
            <Tabs value={curTab} onChange={handleChange}>
                <Tab label="Estatisticas" value="1"/>
                <Tab label="Jogadores" value="2"/>
            </Tabs>
        </Box>
    )
}

export default Games
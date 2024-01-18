import { Sidebar as ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import BurstModeIcon from '@mui/icons-material/BurstMode';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import BatchPredictionIcon from '@mui/icons-material/BatchPrediction';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import ArticleIcon from '@mui/icons-material/Article';
import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Box, Typography } from "@mui/material";
import InstagramIcon from '@mui/icons-material/Instagram';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GitHubIcon from '@mui/icons-material/GitHub';



const SidebarItem = ({ title, to, icon, selected, setSelected }) => {
    const [isHovered, setIsHovered] = useState(false);

    return (
        <Link to={to}>
            <MenuItem
                active={selected === title}
                style={{
                    textAlign: "center",
                    cursor: "pointer",
                    backgroundColor: isHovered ? "rgba(255, 255, 255, 0.1)" : "",
                    // color: "#fff",

                }}
                onClick={() => setSelected(title)}
                icon={React.cloneElement(icon, { style: { color: '#39FF14' } })}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
            >
                <Typography color="#fff">{title}</Typography>
            </MenuItem>
        </Link>
    );
};

const CustomSidebar = () => {
    const [isCollapsed, setIsCollapsed] = useState(false);
    const [isHovered, setIsHovered] = useState(false);
    const [selected, setSelected] = useState("");



    return (
        <div
            id="app"
            style={{
                height: "100vh",
                display: "flex",
            }}
        >
            <ProSidebar
                collapsed={isCollapsed}
                style={{
                    height: "100vh",
                    cursor: "pointer",
                    backgroundColor: isHovered ? "#fffff" : "",
                }}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                backgroundColor="#fffff"
            >
                <Menu iconShape="square">
                    <MenuItem
                        onClick={() => setIsCollapsed(!isCollapsed)}
                        icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
                        style={{
                            textAlign: "justify",
                            cursor: "pointer",
                            backgroundColor: isHovered ? "rgba(255, 255, 255, 0.1)" : "",


                        }}
                        onMouseEnter={() => setIsHovered(true)}
                        onMouseLeave={() => setIsHovered(false)}
                    >
                        <Typography>Weapon Detection</Typography>
                    </MenuItem>

                    <SidebarItem
                        icon={<BurstModeIcon />}

                        title={'Image Capture'
                        }
                        to='/capture'
                        selected={selected}
                        setSelected={setSelected}
                    />
                    <SidebarItem
                        icon={<BatchPredictionIcon />}

                        to='/load'
                        title={"Image Load"}
                        selected={selected}
                        setSelected={setSelected}
                    />

                    <SidebarItem
                        icon={<ArticleIcon />}

                        to="/log"
                        title={"Log Read"}
                        selected={selected}
                        setSelected={setSelected}
                    />




                    <SidebarItem
                        icon={<InsertDriveFileIcon />}

                        to='/documentation'
                        title={"Documentation"}
                        selected={selected}
                        setSelected={setSelected}
                    />

                    <div style={{
                        display: 'flex',
                        flexDirection: isCollapsed ? 'column' : 'row',
                        justifyContent: 'space-around',
                        padding: '1em',
                        position: 'absolute',
                        bottom: 0,
                        width: '90%'
                    }}>
                        <a href="https://www.linkedin.com/in/ishworrsubedii/" target="_blank" rel="noopener noreferrer">
                            <LinkedInIcon style={{ color: '#39FF14' }} />
                        </a>
                        <a href="https://github.com/ishworrsubedii" target="_blank" rel="noopener noreferrer">
                            <GitHubIcon style={{ color: '#39FF14' }} />
                        </a>
                        <a href="https://www.instagram.com/ishworr__/" target="_blank" rel="noopener noreferrer">
                            <InstagramIcon style={{ color: '#39FF14' }} />
                        </a>
                    </div>


                </Menu>
            </ProSidebar>

        </div>
    );
};

export default CustomSidebar;
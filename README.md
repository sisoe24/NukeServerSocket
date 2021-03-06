# 1. NukeServerSocket README

[![Main Build](https://img.shields.io/github/v/release/sisoe24/NukeServerSocket?label=stable)](https://github.com/sisoe24/NukeServerSocket/releases)
[![Pre Release](https://img.shields.io/github/v/release/sisoe24/NukeServerSocket?label=pre-release&include_prereleases)](https://github.com/sisoe24/NukeServerSocket/releases)
![Last commit](https://img.shields.io/github/last-commit/sisoe24/NukeServerSocket)

[![issues](https://img.shields.io/github/issues/sisoe24/NukeServerSocket)](https://github.com/sisoe24/NukeServerSocket/issues)
[![pull-request](https://img.shields.io/github/issues-pr/sisoe24/NukeServerSocket)](https://github.com/sisoe24/NukeServerSocket/pulls)

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/5b59bd7f80c646a8b2b16ad4b8cba599)](https://www.codacy.com/gh/sisoe24/NukeServerSocket/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sisoe24/NukeServerSocket&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/5b59bd7f80c646a8b2b16ad4b8cba599)](https://www.codacy.com/gh/sisoe24/NukeServerSocket/dashboard?utm_source=github.com&utm_medium=referral&utm_content=sisoe24/NukeServerSocket&utm_campaign=Badge_Coverage)
[![DeepSource](https://deepsource.io/gh/sisoe24/NukeServerSocket.svg/?label=active+issues&show_trend=true&token=D3BtO5z54YqAh2Fn2pTf9JKB)](https://deepsource.io/gh/sisoe24/NukeServerSocket/?ref=repository-badge)

[![license](https://img.shields.io/github/license/sisoe24/NukeServerSocket)](https://github.com/sisoe24/NukeServerSocket/blob/main/LICENSE)

![x](https://img.shields.io/badge/Python-2.7.18_|_3.7.7-success)
![x](https://img.shields.io/badge/Nuke-11_|_12_|13-yellow)

A Nuke plugin that lets you execute code from a text editor in your local network and more.

- [1. NukeServerSocket README](#1-nukeserversocket-readme)
  - [1.2. Features](#12-features)
  - [1.1. Client applications](#11-client-applications)
  - [1.3. Installation](#13-installation)
  - [1.4. Usage](#14-usage)
    - [1.4.1.Execute code](#141execute-code)
    - [1.4.2. Receive/Send nodes](#142-receivesend-nodes)
  - [1.5. Settings](#15-settings)
  - [1.6. Extendibility](#16-extendibility)
  - [1.7. Test plugin locally](#17-test-plugin-locally)
  - [1.8. Known Issues](#18-known-issues)
  - [1.9. Compatibility](#19-compatibility)
  - [1.10. Demo](#110-demo)

## 1.2. Features

- Send Python or BlinkScript code to be executed inside Nuke from your local network.
- Multiple computers can connect to the same Nuke instance.
- Receive/Send nodes from another Nuke instance in your local network.
- Easy integration with custom clients. (more on [Extendibility](#16-extendibility))
- WebSocket-compatible for browser-based text editors.

## 1.1. Client applications

Client applications that can use NukeServerSocket:

- [Nuke Tools](https://marketplace.visualstudio.com/items?itemName=virgilsisoe.nuke-tools) - Visual Studio Code extension.
- [Nuke Tools ST](https://packagecontrol.io/packages/NukeToolsST) - Sublime Text package.
- [DCC WebSocket](https://marketplace.visualstudio.com/items?itemName=virgilsisoe.dcc-websocket) - Visual Studio Code Web extension.

## 1.3. Installation

1. Download the repository via the releases page or by cloning it from GitHub.
2. Move the folder inside your _~/.nuke_ directory or into a custom one.
3. Write `import NukeServerSocket` into your _menu.py_.  

NOTES

- If you use a custom plugin path, add the path in your init.py: `nuke.pluginAddPath('custom/path')`
- The folder name must be named **NukeServerSocket**.

## 1.4. Usage

### 1.4.1.Execute code

![Execute Code](images/execute_code.gif)

1. Open the NukeServerSocket panel inside Nuke, and with the mode on **Receiver**, start the server by clicking **Connect**.
2. You can now send code from Visual Studio Code with [Nuke Tools](https://marketplace.visualstudio.com/items?itemName=virgilsisoe.nuke-tools) or any other method you prefer.

NOTES:

- You can troubleshoot the connection with the **Test Receiver** button.
- If you receive a message: "_Server did not initiate. Error: The bound address is already in use_", change the **port** to a random number between `49152` and `65535` and try again. It probably means that you have a connection listening on that port already.

### 1.4.2. Receive/Send nodes

![Send Nodes](images/send_nodes.gif)

- Receive

   When receiving nodes, you only need to start the Server ([Receive incoming request](#141-receive-incoming-request)).

- Send

  1. When sending nodes, switch the mode from **Receiver** to **Sender** and be sure that there is another NukeServerSocket instance listening for incoming network request ([Receive incoming request](#141-receive-incoming-request)).
  2. Select the nodes you want to send a click **Send Selected Nodes**.

NOTES:

- When sending nodes on the same computer, only the **Port** value must match the two Nuke instances.
- When sending nodes between different computers, both **IP Address** and **Port** must match the two Nuke instances.

## 1.5. Settings

Accessing the settings can be done from the plugin toolbar.

- **Code Execution Engine**: Change the engine that will be executing the code.
  - **Nuke Internal**: Nuke `executeInMainThread` function. [**Default**]
  - **Script Editor**: Nuke Script Editor widget.

  > Why use one over the other?
  >
  > - Nuke Internal uses a more direct and fast approach, but it does not handle internal exceptions and modal windows very well.
  > - Nuke Script Editor uses a safer approach overall, but it does require slightly more work behind the scene.

- **Connection Type**: Change the internal connection protocol for the client-server.
  - **TCP**: The default type of connection. If unsure, use this. [**Default**]
  - **WebSocket**: This allows a two-way interactive communication session between the user's browser and the internal server. Use this when using a browser-based text editor.

  **NOTE**: Changing connection type while connected could cause some errors.

- **Mirror To Script Editor**: Allows mirroring the input/output code to the internal script editor.
  - **Override Output Editor**: Mirror output to the internal script editor.
  - **Format Text**: The script editor output window will receive a formatted version of the code result.
  - **Clear Output**:  The script editor output window will clear the code after each execution.
  - **Show File Path**: The script editor output window will display the full path for the executed file.
  - **Show Unicode**: The script editor output window will display a Unicode character `` that indicates the start of the code execution result.
  - **Override Input Editor**: Mirror input to the internal script editor.

- **Timeout**: Terminate the connection when the Server is inactive or did not establish a successful contact in the time specified.
  - **Server**: Set the Timeout when clicking the **Connect** button. The default value is `10` minutes.
  - **Receiver**: Set the Timeout for when clicking the **Test Receiver** button. The default value is `10` seconds.
  - **Send Nodes**: Set the Timeout when clicking **Send Nodes** button. The default value is `30` seconds.

## 1.6. Extendibility

At its core, the plugin is just a server socket that waits for an incoming request,
performs the operations inside Nuke, and returns the result. Nothing ties it to any application per se.

This makes it very easy to implement a new client, without the need to modify the NukeServerSocket source code. The client needs only to send the data at the specified address inside NukeServerSocket.

You can find more information and examples on the [wiki page](https://github.com/sisoe24/NukeServerSocket/wiki/Create-custom-client).

## 1.7. Test plugin locally

You can run the plugin locally outside the Nuke application. This method is handy for testing code and implementing new features faster.

You can find more information and examples on the [wiki page](https://github.com/sisoe24/NukeServerSocket/wiki/Test-Plugin-locally).

## 1.8. Known Issues

- Creating a modal window with the Nuke internal code execution engine will cause Nuke to freeze. A workaround is to switch to the Script Editor engine.
- Settings window doesn't display the tooltip text.
- Changing workspace with an active open connection makes Nuke load a new plugin instance with the default UI state. So it would look as if the previous connection has been closed, whereas in reality is still open and listening. To force close all of the listening connections, you can:
  - Restart the Nuke instance.
  - Wait for the connection timeout.

## 1.9. Compatibility

Nuke version: 11,12, 13.

> Because Nuke 11 uses an early version of PySide2, future compatibility is not a guarantee.

While it should work the same on all platforms, I have tested the plugin only on:

- Linux:
  - CentOS 8
- macOS:
  - Mojave 10.14.06
  - Catalina 10.15.07
- Windows 10

## 1.10. Demo

Execute code from Visual Studio Code

![Execute Code](images/execute_code.gif)

Send nodes

![Send Nodes](images/send_nodes.gif)

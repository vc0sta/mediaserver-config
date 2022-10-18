/*
Title: SSH Configuration
Description: SSH Configuration
Sort: 0
*/

To configure SSH on your Respberry Pi, youo will need to enable sshd service in it:

![Enabling SSH](../images/ssh-enable.gif)

Then add your public keys to *~/.ssh/authorized_keys*:

```sh
touch ~/.ssh/authorized_keys
curl https://github.com/your-username.keys >> ~/.ssh/authorized_keys
```

> **Note:** If you don't have SSH keys configured yet, you can follow GitHub documentation [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and [here](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

**[Optional]** Create an entry in *~/.ssh/config* in your machine:

```
Host raspi
  HostName 192.168.77.104
  User pi
  IdentityFile ~/.ssh/id_rsa
```

With everything in place, you can SSH into RaspberryPi by using:

```
ssh raspi
```
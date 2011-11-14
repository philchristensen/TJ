TJ, a Twisted Jabber bot 1.0
===========

14 November 2011

by Phil Christensen

`mailto:phil@bubblehouse.org`

Introduction
-------------

A few weeks ago, GitHub released their internal bot tool, Hubot to the world, and
everyone thought it was awesome. I thought it was nice in theory, but in practice
using it was a pain. Here are the things I didn't like about Hubot that I'm trying
to fix in TJ:

* **Python Architecture**  — 
  Node is a fascinating project, and I'm extremely excited by how it's exposing
  a whole generation of web programmers about asynchronous development. I'm also
  a fan of Javascript, at least when it's targeted towards a specific platform.
  Node is still in its infancy, though, and can't compare with the maturity of
  the libraries available for Python, particularly Twisted.

* **Runs as Daemon** — 
  Hubot doesn't provide *any* functionality for daemonizing itself. Output doesn't
  contain timestamps, and the service doesn't save a pidfile. Check out [this
  horrifying piece of bash](https://gist.github.com/1352381) to see what I had to go through to deal with hubot.

* **"High-availability"** —
  Chatbots seem to tend towards flaky code, but it's not acceptable for a poorly
  written plugin to crash the server. Neither should the bot get disconnected
  permanently due to transient server issues, like lost connections.

By selecting Twisted as a foundation for this project, I get a lot of stuff for
free (daemon mode, logging improvements, plugin support, asynchronous multi-
protocol support, etc.).

Copyright
---------

All code in this distribution is (C) Phil Christensen.

antioch is made available under the MIT/X Consortium license.
The included LICENSE file describes this in detail.

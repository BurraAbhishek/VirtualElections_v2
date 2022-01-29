# Licensing FAQs

In case you find any ambiguities in the Licensing Terms, or if you're confused, you can find all the answers to your questions here. 
In case your problem is not listed here, you may either create a GitHub issue, or you may choose to send an email.

## Is this source code compliant with the GNU Affero General Public License?

Yes. You can view the source code of the website by going to `/source`. See [urls.py](https://github.com/BurraAbhishek/VirtualElections_v2/blob/main/virtualelections_v2/urls.py) for more information.

## I want all those who use my source code to release their source code to their users.

Clearly mention either in your README or update the License to show that your fork exclusively uses the GNU Affero General Public License. Please note that while all your freedoms are guaranteed, dependents need not release their source code as long as they refer to either this repository or any source which is not exclusively licensed under the AGPL.

Please note that any fork which has a dependency strictly licensed under the GNU AGPL will solely be licensed 
under the GNU AGPL, and you must release your source code in those cases. No exceptions will apply in such cases, even if your organization disallows AGPL source code, unless the owner of that fork gives explicit permission to not disclose your source code. This repository does NOT contain any such dependency.

## My organization strictly disallows AGPL source code, but I want to use your source code.

You may have to obtain permission from your organization to use this source code.
In all such cases, the Terms of the Apache License, Version 2.0 are binding. You are permitted to keep the resulting source code proprietary (closed-source).
In addition to that, clearly mention somewhere in your software that this dependency or source code is licensed under the Terms of the Apache License, Version 2.0.
You may also want to reflect the same by removing the `/source` link in `urls.py` in your copy, if you wish to keep your copy closed-source.

## In that case, won't just the Apache License, Version 2.0 be sufficient?

It definitely will be sufficient. However, since the [PHP-SQL version](https://github.com/BurraAbhishek/VirtualElections) of this software was licensed under the GNU Affero General Public License at some point of time, we want to extend the dual license to the [Django version](https://github.com/BurraAbhishek/VirtualElections_v2) of this software. Also, using AGPL as an option shows that this [original source code can be viewed by the users of this software, even when distributed over a network](https://github.com/BurraAbhishek/VirtualElections_v2/blob/main/templates/docs/source.html).

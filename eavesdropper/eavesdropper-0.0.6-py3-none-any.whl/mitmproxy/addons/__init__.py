from eavesdropper.mitmproxy.addons import anticache
from eavesdropper.mitmproxy.addons import anticomp
from eavesdropper.mitmproxy.addons import block
from eavesdropper.mitmproxy.addons import browser
from eavesdropper.mitmproxy.addons import check_ca
from eavesdropper.mitmproxy.addons import clientplayback
from eavesdropper.mitmproxy.addons import command_history
from eavesdropper.mitmproxy.addons import core
from eavesdropper.mitmproxy.addons import cut
from eavesdropper.mitmproxy.addons import disable_h2c
from eavesdropper.mitmproxy.addons import export
from eavesdropper.mitmproxy.addons import onboarding
from eavesdropper.mitmproxy.addons import proxyauth
from eavesdropper.mitmproxy.addons import script
from eavesdropper.mitmproxy.addons import serverplayback
from eavesdropper.mitmproxy.addons import mapremote
from eavesdropper.mitmproxy.addons import maplocal
from eavesdropper.mitmproxy.addons import modifybody
from eavesdropper.mitmproxy.addons import modifyheaders
from eavesdropper.mitmproxy.addons import stickyauth
from eavesdropper.mitmproxy.addons import stickycookie
from eavesdropper.mitmproxy.addons import streambodies
from eavesdropper.mitmproxy.addons import save
from eavesdropper.mitmproxy.addons import upstream_auth


def default_addons():
    return [
        core.Core(),
        browser.Browser(),
        block.Block(),
        anticache.AntiCache(),
        anticomp.AntiComp(),
        check_ca.CheckCA(),
        clientplayback.ClientPlayback(),
        command_history.CommandHistory(),
        cut.Cut(),
        disable_h2c.DisableH2C(),
        export.Export(),
        onboarding.Onboarding(),
        proxyauth.ProxyAuth(),
        script.ScriptLoader(),
        serverplayback.ServerPlayback(),
        mapremote.MapRemote(),
        maplocal.MapLocal(),
        modifybody.ModifyBody(),
        modifyheaders.ModifyHeaders(),
        stickyauth.StickyAuth(),
        stickycookie.StickyCookie(),
        streambodies.StreamBodies(),
        save.Save(),
        upstream_auth.UpstreamAuth(),
    ]

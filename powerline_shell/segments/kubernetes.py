# -*- coding: utf-8 -*-
"""The kubernetes segment shows current k8s context and namespace

Requires the kubectl command to be installed. If kubectl is not installed, the segment will show nothing.

If the context is not set, the segment will show nothing.
"""
import subprocess
from ..utils import BasicSegment


def get_context_cmd(prop):
    return ("kubectl config view --minify -o jsonpath='{..context.%s}'" % prop).split()


def get_context_property(prop):
    args = get_context_cmd(prop)
    output = subprocess.check_output(args, encoding="utf-8", stderr=subprocess.DEVNULL)
    return output.strip().strip("'")


def get_kubeinfo():
    try:
        ctx = get_context_property("cluster")
        ns = get_context_property("namespace")

        return f' \u2638 {ctx}:{ns} '
    except Exception:
        return None


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            kubeinfo = get_kubeinfo()
            if kubeinfo is not None:
                powerline.append(kubeinfo, self.powerline.theme.KUBERNETES_FG, self.powerline.theme.KUBERNETES_BG)
        except OSError:
            return

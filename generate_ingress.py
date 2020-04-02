#!/usr/bin/env python3

import jinja2
import argparse
import petname

class Ingress_Generator():
  def __init__(self, templates_path, namespace_count, host_count,
              path_count, tls_ratio, deployment_name, deployment_image, deployment_replicas, ingress_domain):

    self.namespace_count = namespace_count
    self.host_count = host_count
    self.path_count = path_count
    self.tls_ratio = tls_ratio

    self.deployment_name = deployment_name
    self.deployment_image = deployment_image
    self.deployment_replicas = deployment_replicas

    self.ingress_domain = ingress_domain
    self.templates_path = templates_path

    self.namespace_list = []
    for i in range(1,self.namespace_count + 1):
      name = petname.generate(1) + str(i)
      self.namespace_list.append(name)

    self.path_list = []
    for i in range(1,self.path_count + 1):
      name = petname.generate(1) + str(i)
      self.path_list.append(name)

    self.generate_host_path()
    if args.path_count > 1:
      self.generate_host_mpath()


  def generate_host_path(self):
    file_loader = jinja2.FileSystemLoader(self.templates_path)
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template('ingress-host-path.j2')
    for namespace in self.namespace_list:
      for idx in range(1,self.host_count + 1):
        output = template.render(deployment_name=self.deployment_name,
                                      deployment_image=self.deployment_image,
                                      deployment_replicas=self.deployment_replicas,
                                      deployment_namespace=namespace,
                                      idx = petname.generate(1) + str(idx),
                                      ingress_domain=self.ingress_domain)
        print(output)

  def generate_host_mpath(self):
    file_loader = jinja2.FileSystemLoader(self.templates_path)
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template('ingress-host-mpath.j2')
    for namespace in self.namespace_list:
      for idx in range(1,self.host_count + 1):
        output = template.render(deployment_name=self.deployment_name,
                                      deployment_image=self.deployment_image,
                                      deployment_replicas=self.deployment_replicas,
                                      deployment_namespace=namespace,
                                      idx = petname.generate(1) + str(idx),
                                      ingress_domain=self.ingress_domain,
                                      path_list = self.path_list)
        print(output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingress Generator')
    parser.add_argument("--templates-path",
                        dest='templates_path', default='templates')

    parser.add_argument("-c --namespace-count",
                        dest='namespace_count', type=int, default=10)
    parser.add_argument("-n --host-count", help='Count of unique Host headers',
                        dest='host_count', type=int, default=10)
    parser.add_argument("-m --path-count", help='Count of path under unique host header',
                        dest='path_count', type=int, default=10)
    parser.add_argument("-r --tls-ratio",
                        dest='tls_ratio', type=int, default=0.5)

    parser.add_argument("--deployment_name",
                        dest='deployment_name', default='kuard')
    parser.add_argument("--deployment_image",
                        dest='deployment_image', default='gcr.io/kuar-demo/kuard-amd64:1')
    parser.add_argument("--deployment_replicas",
                        dest='deployment_replicas', type=int, default=3)

    parser.add_argument("--ingress-domain",
                        dest='ingress_domain', default='ako.capv-cluster.cs.lab')

    args = parser.parse_args()

    ingress_generator = Ingress_Generator(templates_path = args.templates_path,
                                          namespace_count = args.namespace_count,
                                          host_count = args.host_count,
                                          path_count = args.path_count,
                                          tls_ratio = args.tls_ratio,
                                          deployment_name = args.deployment_name,
                                          deployment_image = args.deployment_image,
                                          deployment_replicas = args.deployment_replicas,
                                          ingress_domain = args.ingress_domain
                                          )
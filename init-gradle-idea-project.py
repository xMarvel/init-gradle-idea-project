# -*- coding: utf-8 -*-
import sys
import os
import logging
import subprocess
import argparse

logging.basicConfig(level=logging.DEBUG)


def create_dir(artifact_id):
    current_path = os.getcwd()
    project_path = os.path.join(current_path, artifact_id)
    if os.path.exists(project_path):
        logging.error('ProjectDir:{} is existed'.format(project_path))
        sys.exit(1)
    else:
        os.mkdir(project_path)
        logging.info('ProjectDir:{} is created'.format(project_path))


def gradle_init(artifact_id):
    os.chdir(artifact_id)
    logging.info(os.getcwd())
    try:
        subprocess.run(["gradle", "init"], check=True)
        logging.info('gradle init')
    except subprocess.CalledProcessError as e:
        logging.error('gradle init error:{}'.format(e))
        sys.exit(1)


def gradle_build_edit():
    build_content = """
    apply plugin: 'java'
    apply plugin: 'idea'

    sourceCompatibility = 1.8
    targetCompatibility = 1.8
    
    buildscript {
        ext {
            springBootVersion = "1.5.7.RELEASE"
        }
        repositories {
            jcenter()
        }
        dependencies {
            classpath("org.springframework.boot:spring-boot-gradle-plugin:${springBootVersion}")
        }
    }
    
    repositories {
        jcenter()
    }
    
    dependencies {
        compile "org.springframework.boot:spring-boot-starter-web:${springBootVersion}"
        compile "org.springframework.boot:spring-boot-starter-data-jpa:${springBootVersion}"
        compile "mysql:mysql-connector-java:5.1.39"
        testCompile "junit:junit"
    }
    """
    logging.info('edit build.gradle')
    with open(os.path.join(os.getcwd(), 'build.gradle'), mode="w", encoding='utf-8') as f:
        try:
            f.write(build_content)
        except Exception as e:
            logging.error('Modify build.gradle error:{}'.format(e))
            sys.exit(1)

# def sub(text):
#     return text.format_map(safesub(sys._getframe(1).f_locals))

def mk_project_dir_file(group_id, artifact_id):
    current_path = os.getcwd()
    # create code directory
    package_path = 'src/main/java/' + group_id.replace('.', '/') + '/' + artifact_id
    code_path = os.path.join(current_path, package_path)
    res_path = os.path.join(current_path, 'src/main/resources')
    os.makedirs(code_path)
    os.makedirs(res_path)
    # 创建application.java
    application_code = """
    package com.example.%s;
    
    import org.springframework.boot.SpringApplication;
    import org.springframework.boot.autoconfigure.SpringBootApplication;
    
    @SpringBootApplication
    public class Application {
        public static void main(String[] args) {
            SpringApplication.run(Application.class, args);
        }
    }
    """%(artifact_id)
    logging.info('create application.java')
    with open(os.path.join(package_path, 'application.java'), mode="w", encoding='utf-8') as f:
        try:
            f.write(application_code)
        except Exception as e:
            logging.error('create application.java error:{}'.format(e))
            sys.exit(1)
    # 创建application.properties
    open(os.path.join(res_path, 'application.properties'), mode="w", encoding='utf-8').close()

    # create test directory
    code_path_test = os.path.join(current_path, 'src/test/java')
    res_path_test = os.path.join(current_path, 'src/test/resources')
    os.makedirs(code_path_test)
    os.makedirs(res_path_test)
    logging.info('make project directory')


def gradle_idea():
    try:
        subprocess.run(["gradle", "idea"], check=True)
        logging.info('gradle idea')
    except subprocess.CalledProcessError as e:
        logging.error('gradle idea error:{}'.format(e))
        sys.exit(1)


def open_idea_project(artifact_id):
    try:
        subprocess.run(["open", artifact_id + ".ipr"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error('open init error:{}'.format(e))
        sys.exit(1)


def init_project(group_id, artifact_id):
    logging.info('Project:{} is begin init'.format(artifact_id))
    create_dir(artifact_id)
    gradle_init(artifact_id)
    gradle_build_edit()
    mk_project_dir_file(group_id, artifact_id)
    gradle_idea()
    open_idea_project(artifact_id)
    logging.info('Project:{} is completed init'.format(artifact_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create spring boot project')
    parser.add_argument('-g', '--group_id', required=True, help='input group_id')
    parser.add_argument("-a", "--artifact_id", required=True, help='input artifact_id')
    args = parser.parse_args()
    init_project(args.group_id, args.artifact_id)

# -*- coding: utf-8 -*-
import sys
import os
import logging
import subprocess
import argparse

logging.basicConfig(level=logging.DEBUG)


def create_dir(projectName):
    currentPath = os.getcwd()
    projectPath = os.path.join(currentPath, projectName)
    if os.path.exists(projectPath):
        logging.error('ProjectDir:{} is existed'.format(projectPath))
        sys.exit(1)
    else:
        os.mkdir(projectPath)
        logging.info('ProjectDir:{} is created'.format(projectPath))


def gradle_init(projectName):
    os.chdir(projectName)
    logging.info(os.getcwd())
    try:
        subprocess.run(["gradle", "init"], check=True)
        logging.info('gradle init')
    except subprocess.CalledProcessError as e:
        logging.error('gradle init error:{}'.format(e))
        sys.exit(1)


def gradle_build_edit():
    buildContent = """
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
            f.write(buildContent)
        except Exception as e:
            logging.error('Modify build.gradle error:{}'.format(e))
            sys.exit(1)


def mkProject_dir_file():
    currentPath = os.getcwd()
    code_path = os.path.join(currentPath, 'src/main/java')
    res_path = os.path.join(currentPath, 'src/main/resources')
    os.makedirs(code_path)
    os.makedirs(res_path)
    open(os.path.join(res_path, 'application.properties'), mode="w", encoding='utf-8').close()
    code_path_test = os.path.join(currentPath, 'src/test/java')
    res_path_test = os.path.join(currentPath, 'src/test/resources')
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


def open_idea_project(projectName):
    try:
        subprocess.run(["open", projectName + ".ipr"],check=True)
    except subprocess.CalledProcessError as e:
        logging.error('open init error:{}'.format(e))
        sys.exit(1)


def init_project(project_name):
    logging.info('Project:{} is begin init'.format(project_name))
    create_dir(project_name)
    gradle_init(project_name)
    gradle_build_edit()
    mkProject_dir_file()
    gradle_idea()
    open_idea_project(project_name)
    logging.info('Project:{} is completed init'.format(project_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create spring boot project')
    parser.add_argument("-p","--projectname", required=True, help='input project name')
    args=parser.parse_args()
    init_project(args.projectname)

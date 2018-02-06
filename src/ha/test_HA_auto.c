#include "ha/HAClient.h"
#include "ha/HAManager.h"
#include "common/AioCompletionImp.h"
#include <iostream>
#include <stdio.h>
#include <fcntl.h>
#include <signal.h>
#include <unistd.h>

#define RUNNING_DIR	"/var/run/"
#define LOCK_FILE	"hdcs.lock"
#define LOG_FILE	"hdcs.log"

void log_message(char* filename, char*message) {
  FILE *logfile;
	logfile=fopen(filename,"a");
	if(!logfile) return;
	fprintf(logfile,"%s\n",message);
	fclose(logfile);
}

void signal_handler(int sig) {
	switch(sig) {
	case SIGHUP:
		log_message(LOG_FILE,"hangup signal catched");
		break;
	case SIGTERM:
		log_message(LOG_FILE,"terminate signal catched");
		exit(0);
		break;
	}
}

void daemonize() {
  int i,lfp;
  char str[10];
	if (getppid()==1)
    return; /* already a daemon */
	i = fork();
	if (i<0)
    exit(1); /* fork error */
	if (i>0)
    exit(0); /* parent exits */
	/* child (daemon) continues */
	setsid(); /* obtain a new process group */
	for (i=getdtablesize();i>=0;--i) close(i); /* close all descriptors */
	i=open("/dev/null",O_RDWR); dup(i); dup(i); /* handle standart I/O */
	umask(027); /* set newly created file permissions */
	chdir(RUNNING_DIR); /* change running directory */
	lfp=open(LOCK_FILE,O_RDWR|O_CREAT,0640);
	if (lfp<0) exit(1); /* can not open */
	if (lockf(lfp,F_TLOCK,0)<0) exit(0); /* can not lock */
	/* first instance continues */
	sprintf(str,"%d\n",getpid());
	write(lfp,str,strlen(str)); /* record pid to lockfile */
	signal(SIGCHLD,SIG_IGN); /* ignore child */
	signal(SIGTSTP,SIG_IGN); /* ignore tty signals */
	signal(SIGTTOU,SIG_IGN);
	signal(SIGTTIN,SIG_IGN);
	signal(SIGHUP,signal_handler); /* catch hangup signal */
	signal(SIGTERM,signal_handler); /* catch kill signal */
}

int main(int argc, char *argv[]) {
  if (argc == 5) {
  } else {
   printf("Usage:\n\t%s -r server/client -n ${name}\n\n", argv[0]);
   return -1;
  }

  hdcs::ha::HAConfig ha_config("");
  std::string cmd;
  std::string node;
  if (argv[2][0] == 'c') {
    hdcs::ha::HAClient ha_client(argv[4], std::move(ha_config));
    ha_client.add_ha_server("host01");
    while (true) {
      printf("Input bye to exit.");
      std::cin >> cmd;
      if (cmd.compare("bye") == 0) break;
    }
  }

  if (argv[2][0] == 's') {
    //daemonize(); 
    hdcs::ha::HAManager ha_mgr(argv[4], std::move(ha_config));
    while (true) {
      printf("Please input your cmd(bye/cmdline): ");
      std::cin >> cmd;
      if (cmd.compare("bye") == 0) break;
      else {
        ha_mgr.process_cmd(cmd);
      }
    }
  }
  return 0;
}

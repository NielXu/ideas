#include "fhook.h"

int main(int argc, char *argv[]) {
    int sleep_interval = 0;
    char *monitor_file = "";
    char *cmd = "";
    int has_cmd = 0;
    if (argc < 3) {
        printf("Usage: ./fhook [monitor_file] [check_interval] (cmd)\n");
        printf("[monitor_file]: required, the file to be monitored for changes\n");
        printf("[check_interval]: required, the interval that the watcher check for changes, lower value will check more constantly\n");
        printf("(cmd): optional, the command to be invoked when a file changes detected\n");
        return 0;
    } else {
        monitor_file = argv[1];
        sleep_interval = atoi(argv[2]);
        if (argc > 3) {
            cmd = argv[3];
            has_cmd = 1;
        }
    }
    printf("Monitoring file: %s\n", monitor_file);
    printf("Watcher active interval: %d\n", sleep_interval);
    if (has_cmd) {
        printf("Script to be executed when file changed: %s\n", cmd);
    }
    printf("\n");

    struct _stat buf;
    int result;
    char timebuf[26];
    char lasttimebuf[26];
    errno_t err;
    int init_lasttimebuf = 0;
    int init_timebuf = 0;

    while (1) {
        // Get data associated with the given file
        result = _stat( monitor_file, &buf );

        // Check if statistics are valid
        if( result != 0 ) {
            perror( "Problem getting information");
            switch (errno) {
                case ENOENT:
                    printf("File %s not found.\n", monitor_file);
                    break;
                case EINVAL:
                    printf("Invalid parameter to _stat.\n");
                    break;
                default:
                    /* Should never be reached. */
                    printf("Unexpected error in _stat.\n");
            }
            exit(1);
        }
        else {
            // Save the last timebuf for comparision
            if (init_timebuf) {
                for (int i = 0; i < 26; i++) {
                    lasttimebuf[i] = timebuf[i];
                }
                init_lasttimebuf = 1;
            }
            err = ctime_s(timebuf, 26, &buf.st_mtime);
            init_timebuf = 1;
            if (err) {
                printf("Invalid arguments to ctime_s.");
                exit(1);
            }
            // Compare if time has changed
            if (init_lasttimebuf && init_timebuf) {
                for (int i = 0; i < 26; i++) {
                    if (lasttimebuf[i] != timebuf[i]) {
                        printf("Changes detected\n");
                        if (has_cmd) {
                            int status = system(cmd);
                            printf("Executed command status: %d\n", status);
                        }
                        printf("\n");
                        break;
                    }
                }
            }
        }
        Sleep(sleep_interval);
    }
    return 0;
}

#include<malloc.h>

#define BLOCK_SIZE 1024*1024*50
#define RUNNING_COUNT 100

int main(void){

	FILE* f;
	time_t t;
	struct timeval starttime, endtime;
	double timeuse;
	int i,j;
	char* tmp;
	char* p = (char*)malloc(BLOCK_SIZE*sizeof(char));
	if(p == NULL){
		printf("malloc error!");
		return -1;
	}
	f = fopen("task_result.txt","a+");
	if(f == NULL){
		printf("file open fail");
		free(p);
		return -1;
	}
	t = time(&t);
	fprintf(f,"\nTaskSim running record: %s\n", ctime(&t));
	for(i=0;i<RUNNING_COUNT;i++){
		tmp = p;
		gettimeofday(&starttime,NULL);
		for(j=0;i<BLOCK_SIZE;j++){
			*tmp = 67;
			tmp++;
		}
		gettimeofday(&endtime,NULL);
		timeuse=1000000*(endtime.tv_sec-starttime.tv_sec)+endtime.tv_usec-starttime.ty_usec;
		fprintf(f,"a block is written, using time %f ms.\n", timeuse/1000);
	}
	printf("Task is over.\n");
	free(p);
	fclose(f);
	return 0;
} 

#include <stdlib.h>
#include <stdio.h>
#include <omp.h>
#include <iomanip>
#include <iostream>
#include <time.h>
#include <math.h>

using namespace std;

double *A, *Q, *R;
double *c, *t;
int n;


void initvector(int *vector, int m);


int main()
{
    int i,j,k,m,thrid,num_threads;
	int qr_eval=1,eval=1; //Debuging FLAGS
	clock_t start, diff;
	double error,d,t_time,s_t_time;
	int *step;
    
    //cout<<"Number of threads: ";
    //cin>>num_threads;
    num_threads=8;
    omp_set_num_threads(num_threads);
    
    A = (double *)malloc(n*n*sizeof(double));
   	t = (double *)malloc(n*n*sizeof(double));
   	Q = (double *)malloc(n*n*sizeof(double));
   	R = (double *)malloc(n*n*sizeof(double));

    n=8;

    step=(int *)malloc(n*sizeof(int));
    initvector(step,n);
    //cout<<step[5];

    double r_sum = 0;
	cout<<"hello1"<<endl;
    srand(time(0));

    #pragma omp parallel private(i,j,k,thrid,r_sum)
	{
		thrid=omp_get_thread_num();
		//cout<<"hello"<<endl;

	   	//Matrix A (initial), matrix 't' a temporary dublicate matrix
	   	//to keep the initial values of A    
        //srand(t_time(0));
	  	#pragma omp for //schedule(static,1)
	  	for (i = 0; i<n; i++)
	  	{
		  	for(j=0;j<n;j++)
		  	{
			  	A[i*n+j] = (rand()%10);
			  	t[i*n+j] = A[i*n+j];			  	
		  	}
		  	step[i]=0;		  	
		}
    	cout<<"hello2"<<endl;
		//set lock = 0
		//unset lock = 1
    	//Parallel version of QR-factorization using 
		//modified Gram-Schmidt algorithm with locks	
		// First column of ( Q[][0] )
		//Thread 0 calculates the 1st column
		//and unsets the 1st lock.
		r_sum=0;
		if(thrid==0)
		{
		// Calculation of ||A||
		for (i=0; i<n; i++){			
			r_sum = r_sum + A[0*n+i] * A[0*n+i]; 
		}
		R[0*n+0] = sqrt(r_sum);  			
		for (i=0; i<n; i++) {
			Q[0*n+i] = A[0*n+i]/R[0*n+0];							
	    	}
	      	//omp_unset_lock(&lock[0]);
            step[0]=1;
		}
		cout<<"hello3"<<endl;
		for (k=1; k<n; k++)
		{
	    	//Check if Q[][i-1] (the previous column) is computed.   	
	   		//omp_set_lock(&lock[k-1]);
        	step[k-1]=1;
	    	//omp_unset_lock(&lock[k-1]);		      
	  		#pragma omp for //schedule(static,1) nowait
			for(j=0; j<n; j++)
			{	
		    	if(step[k-1]==1 && j>=k)
		    	{	    	
			    	R[(k-1)*n+j]=0;	
			    	for(i=0; i<n; i++) 
					{			        	
			        	R[j*n+(k-1)] += Q[(k-1)*n+i] * A[j*n+i];			        	
			    	} 
			        for (i=0; i<n; i++) 
					{				        	
			        	A[j*n+i] = A[j*n+i] - R[j*n+(k-1)]*Q[(k-1)*n+i];
			        }      

					if(j==k)
					{
						thrid=omp_get_thread_num();
						r_sum=0;
						for (i=0; i<n; i++){			
							r_sum = r_sum + A[k*n+i] * A[k*n+i]; 
						}
						R[k*n+k] = sqrt(r_sum); 						
						//#pragma omp for schedule(static,1) nowait
						for (i=0; i<n; i++) {
							Q[k*n+i] = A[k*n+i]/R[k*n+k];			
				      	}
				      	//cout<<"I am thread "<<thrid <<" and step no is"<<k<<"\n";
				      	step[k-1]=0;
                        step[k]=1;

			      	}
		      	}		        
			}			
			r_sum=0;	      	
		}
	}
	cout<<"hello4"<<endl;
    eval=1;
    c = (double *)malloc(n*n*sizeof(double));   	
	cout<<t[0]<<endl;
   	//if(eval==1)
	   {
   		printf("\nPrinting A...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	printf("%.3f ", t[j*n+i]);
		  	}
		  	printf("\n");
		}
	cout<<"hello5"<<endl;
		printf("\nPrinting Q...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	printf("%.3f ", Q[j*n+i]);
		  	}
		  	printf("\n");
		}
	cout<<"hello6"<<endl;
		printf("\nPrinting R...\n");
		for (i = 0; i<n; i++){
		  	for(j=0;j<n;j++){			  	
			  	printf("%.3f ", R[j*n+i]);
		  	}
		  	printf("\n");
		}			
	}	
	
    double sum; 
    
    qr_eval==1;
	//if(qr_eval==1)
	{
		for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {
				sum = 0;
				for (k = 0; k < n; k++) {
					sum = sum + Q[k*n+i] * R[j*n+k];
				}
				c[j*n+i] = sum;
			}
		}
		//if(eval==1)
		{
		printf("\n Q*R (Init A matrix) : \n");
			for (i = 0; i < n; i++) {
				for (j = 0; j < n; j++) {
					printf("%.3f ", c[j*n+i]);
				}
				printf("\n");
			}
		}
		error=0;
		for (i = 0; i < n; i++) {
			for (j = 0; j < n; j++) {				
				error+=fabs(c[j*n+i]-t[j*n+i]);
			}			
		}
		printf("\nError: %e\n",error);
	}	

	//free(A);
    //ree(Q);
   // free(R);
    //free(t);
    //free(c);
   // free(step);

    return 0;


}

void xdoty (double *z, int k, double *y, int m, int ldy, double *x, int ldx)
{
    double s;
    for(int iter=0;iter<k;iter++)
    {
        s=0;

    }
}

void initvector(int *vector, int m)
{
    for(int iter=0;iter<m;iter++)
    {
        vector[iter]=0;

    }

}


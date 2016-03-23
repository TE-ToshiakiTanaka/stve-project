package jp.setsulla.stve.aura;

import android.annotation.SuppressLint;
import android.app.Service;
import android.content.Intent;
import android.os.Handler;
import android.os.IBinder;
import android.os.Message;
import android.support.annotation.Nullable;
import android.util.Log;

import jp.setsulla.stve.aura.debug.Debug;
import jp.setsulla.stve.aura.generic.ExecuteTasksFinishedNotificationRunnable;
import static jp.setsulla.stve.aura.generic.ExecuteTasksFinishedNotificationRunnable.MSG_EXECUTE_TASKS_DONE;

/**
 * Created by setsulla on 2016/02/28.
 */
public class AuraService extends Service {
    public static final String APP_TAG = "Aura";
    private static final String TAG = AuraService.class.getSimpleName();
    public static final int PACKAGE_NAME_LEN = 24;

    public static final String EXECUTE_TASKS_DONE = "jp.setsulla.stve.aura.EXECUTE_TASKS_DONE";
    public static final String KEY_WAIT_TIME = "wait_time";
    public static final String KEY_ACTION_RESULT = "action-result";

    private IRunnableFactory mRunnableFactory;
    private IRunnableTaskExecutor mRunnableTaskExecutor;

    private final ServiceHandler mServiceHandler = new ServiceHandler();

    @Override
    public void onCreate() {
        if (Debug.isDevelopmentEnabled()) {
            Log.d(APP_TAG, TAG + " onCreate()");
        }
        mRunnableFactory = RunnableFactory.createNewFactory(getApplicationContext(), mServiceHandler);
        mRunnableTaskExecutor = RunnableTaskExecutor.createNewExecutor();
        super.onCreate();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (Debug.isDevelopmentEnabled()) {
            Log.d(APP_TAG, TAG + " onStartCommand(), intent [ " + intent + " ] ");
        }
        int startMode = START_NOT_STICKY;
        if (intent != null) {
            startMode = START_STICKY;
            String action = intent.getAction();
            Log.d(APP_TAG, action);
            String[] token = action.split("\\.", 0);
            Log.d(APP_TAG, "Receive a request to run command " + token[token.length - 1]);
            String command = token[token.length - 1];
            Log.d(APP_TAG, TAG + " " + action + " : " + command);
            Runnable runner = mRunnableFactory.build(intent);
            if (runner != null) {
                mRunnableTaskExecutor.submitTask(runner);
                ExecuteTasksFinishedNotificationRunnable executeTasks = new ExecuteTasksFinishedNotificationRunnable(startId);
                mRunnableTaskExecutor.submitTask(new LogRunnable(executeTasks, "TASK_FINISHED_NOTIFIER"));
                mRunnableTaskExecutor.execute();
            } else {
                Log.w(APP_TAG, TAG + " onStartCommand(), Unknown intent, thrown away !");
            }
        }
        return startMode;
    }

    @Override
    public void onDestroy() {
        if (Debug.isDevelopmentEnabled()) {
            Log.d(APP_TAG, TAG + " onDestory()");
        }
        mRunnableTaskExecutor.shutdown();
        super.onDestroy();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @SuppressLint("HandlerLeak")
    private class ServiceHandler extends Handler {
        private int actionId;

        public ServiceHandler() {
            Action action = Action.getActionFromValue(MSG_EXECUTE_TASKS_DONE);
            actionId = Action.getActionId(action);
        }

        @Override
        public void handleMessage(Message msg) {
            String intentAction = mRunnableFactory.getIntentAction(msg);
            boolean actionResult = mRunnableFactory.getActionResult(msg);
            Intent origIntent = mRunnableFactory.getOriginalIntent(msg);
            if (origIntent != null) {
                if (Debug.isUserEnabled()) {
                    Log.d(APP_TAG, TAG + " recieved msg [ " + intentAction + " ] with result [ "
                            + actionResult + " ] from intent [ " + origIntent + " ]");
                }
                origIntent.putExtra(KEY_ACTION_RESULT, actionResult);
                getApplicationContext().sendBroadcast(origIntent);
            }

            if (msg.what == actionId) {
                int startId = msg.arg2;
                Intent done = new Intent(EXECUTE_TASKS_DONE);
                getApplicationContext().sendBroadcast(done);
                AuraService.this.stopSelf(startId);
            }
        }
    }

}

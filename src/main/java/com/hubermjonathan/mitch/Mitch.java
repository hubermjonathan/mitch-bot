package com.hubermjonathan.mitch;

import com.hubermjonathan.mitch.status.StatusLoop;
import com.hubermjonathan.mitch.welcome.WelcomeEvents;
import net.dv8tion.jda.api.JDA;
import net.dv8tion.jda.api.JDABuilder;
import net.dv8tion.jda.api.requests.GatewayIntent;

import javax.security.auth.login.LoginException;
import java.util.Timer;

public class Mitch {
    public static void main(String[] args) throws LoginException {
        JDA jda = JDABuilder.createDefault(System.getenv("TOKEN")).enableIntents(GatewayIntent.GUILD_MEMBERS).build();

        jda.addEventListener(new Dispatcher());
        jda.addEventListener(new WelcomeEvents());

        Timer timer = new Timer();
        timer.schedule(new StatusLoop(jda.getPresence()), 0 , 60 * 60 * 1000);
    }
}
